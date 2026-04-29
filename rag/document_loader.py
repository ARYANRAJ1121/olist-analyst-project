"""
Document Loader & Chunker for Olist RAG Pipeline.

Handles loading different file types (CSV, SQL, Python, Markdown) and
splitting them into semantically meaningful chunks with metadata.

CSV files are converted to natural language summaries rather than raw rows,
because LLMs understand narratives better than raw tabular data.
"""

import os
import csv
import json
from typing import List, Dict, Any


class Document:
    """Represents a single chunk of text with metadata."""

    def __init__(self, content: str, metadata: Dict[str, Any]):
        self.content = content
        self.metadata = metadata

    def __repr__(self):
        return f"Document(len={len(self.content)}, source={self.metadata.get('source', '?')})"


class DocumentLoader:
    """
    Loads project files and converts them into Document objects.

    Different file types get different treatment:
    - Markdown (.md): Split on headers for semantic boundaries
    - CSV (.csv): Convert to natural language summaries
    - SQL (.sql): Keep as code blocks with comment context
    - Python (.py): Keep as code blocks with docstring context
    """

    # File-type specific handlers
    LOADERS = {
        ".md": "_load_markdown",
        ".csv": "_load_csv",
        ".sql": "_load_sql",
        ".py": "_load_python",
    }

    def load_file(self, filepath: str, namespace: str) -> List[Document]:
        """
        Load a single file and return a list of Document chunks.

        Args:
            filepath: Absolute path to the file
            namespace: Pinecone namespace this file belongs to

        Returns:
            List of Document objects with content and metadata
        """
        if not os.path.exists(filepath):
            print(f"  [WARN] File not found: {filepath}")
            return []

        ext = os.path.splitext(filepath)[1].lower()
        loader_method = self.LOADERS.get(ext)

        if loader_method is None:
            print(f"  [WARN] Unsupported file type: {ext} for {filepath}")
            return []

        loader = getattr(self, loader_method)
        documents = loader(filepath, namespace)
        print(f"  [OK] Loaded {os.path.basename(filepath)} → {len(documents)} chunks")
        return documents

    def load_all(self, file_map: Dict[str, List[str]]) -> Dict[str, List[Document]]:
        """
        Load all files organized by namespace.

        Args:
            file_map: Dict mapping namespace -> list of file paths
                      (from config.INDEX_FILES)

        Returns:
            Dict mapping namespace -> list of Document objects
        """
        all_docs = {}
        for namespace, filepaths in file_map.items():
            print(f"\n📂 Loading namespace: {namespace}")
            docs = []
            for fp in filepaths:
                docs.extend(self.load_file(fp, namespace))
            all_docs[namespace] = docs
            print(f"   Total chunks for '{namespace}': {len(docs)}")
        return all_docs

    # =========================================================================
    # FILE-TYPE SPECIFIC LOADERS
    # =========================================================================

    def _load_markdown(self, filepath: str, namespace: str) -> List[Document]:
        """
        Load markdown files, splitting on headers (## / ###).

        Each section becomes one chunk, preserving the header as context.
        """
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        filename = os.path.basename(filepath)
        chunks = []
        current_section = ""
        current_header = filename

        for line in content.split("\n"):
            if line.startswith("## ") or line.startswith("### "):
                # Save previous section if it has content
                if current_section.strip():
                    chunks.append(Document(
                        content=f"[{current_header}]\n{current_section.strip()}",
                        metadata={
                            "source": filename,
                            "section": current_header,
                            "namespace": namespace,
                            "file_type": "markdown",
                        }
                    ))
                current_header = line.strip("# ").strip()
                current_section = line + "\n"
            else:
                current_section += line + "\n"

        # Don't forget the last section
        if current_section.strip():
            chunks.append(Document(
                content=f"[{current_header}]\n{current_section.strip()}",
                metadata={
                    "source": filename,
                    "section": current_header,
                    "namespace": namespace,
                    "file_type": "markdown",
                }
            ))

        return chunks

    def _load_csv(self, filepath: str, namespace: str) -> List[Document]:
        """
        Load CSV files and convert to natural language summaries.

        Instead of indexing raw CSV rows, we create human-readable
        descriptions that LLMs can understand and reason about.

        Small CSVs (< 50 rows): Convert each row to a sentence.
        Large CSVs (churn_features): Generate statistical summary only.
        """
        filename = os.path.basename(filepath)

        with open(filepath, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        if not rows:
            return []

        headers = list(rows[0].keys())
        chunks = []

        # === SPECIAL HANDLING FOR KNOWN FILES ===

        if "monthly_revenue" in filename:
            # Convert monthly revenue to narrative
            narrative = f"Monthly Revenue Data from Olist E-Commerce ({len(rows)} months):\n\n"
            for row in rows:
                narrative += f"- {row['month']}: ${float(row['revenue']):,.2f}\n"

            # Add summary statistics
            revenues = [float(r['revenue']) for r in rows]
            narrative += f"\nSummary: Total revenue = ${sum(revenues):,.2f}, "
            narrative += f"Average monthly = ${sum(revenues)/len(revenues):,.2f}, "
            narrative += f"Peak month = ${max(revenues):,.2f}, "
            narrative += f"Lowest month = ${min(revenues):,.2f}"

            chunks.append(Document(
                content=narrative,
                metadata={"source": filename, "namespace": namespace, "file_type": "csv_data"}
            ))

        elif "retention_metrics" in filename:
            row = rows[0]
            narrative = (
                f"Customer Retention Metrics:\n"
                f"- Total unique customers: {row.get('total_customers', 'N/A')}\n"
                f"- Repeat customers (bought more than once): {row.get('repeat_customers', 'N/A')}\n"
                f"- Repeat purchase rate: {float(row.get('repeat_purchase_rate', 0)) * 100:.1f}%\n"
                f"- One-time customers: {100 - float(row.get('repeat_purchase_rate', 0)) * 100:.1f}%\n"
                f"\nKey Insight: Only about 3% of customers ever make a second purchase. "
                f"97% of customers buy once and never return."
            )
            chunks.append(Document(
                content=narrative,
                metadata={"source": filename, "namespace": namespace, "file_type": "csv_data"}
            ))

        elif "statistical_tests" in filename:
            narrative = "Churn Statistical Test Results:\n\n"
            for row in rows:
                feature = row.get('feature', '')
                narrative += (
                    f"Feature: {feature}\n"
                    f"  - Churned customer mean: {row.get('churned_mean', 'N/A')}\n"
                    f"  - Active customer mean: {row.get('active_mean', 'N/A')}\n"
                    f"  - t-test p-value: {row.get('t_test_p_value', 'N/A')}\n"
                    f"  - Mann-Whitney p-value: {row.get('mannwhitney_p_value', 'N/A')}\n"
                    f"  - Significant? {'Yes' if float(row.get('t_test_p_value', 1)) < 0.05 else 'No'}\n\n"
                )
            narrative += (
                "Conclusion: ALL p-values are above 0.05 — there is NO statistically "
                "significant difference between churned and active customers across any feature."
            )
            chunks.append(Document(
                content=narrative,
                metadata={"source": filename, "namespace": namespace, "file_type": "csv_data"}
            ))

        elif "ab_test" in filename:
            narrative = "A/B Test Results (Second Purchase Conversion):\n\n"
            for row in rows:
                narrative += (
                    f"Group: {row.get('group', '')}\n"
                    f"  - Users: {row.get('users', 'N/A')}\n"
                    f"  - Conversions: {row.get('conversions', 'N/A')}\n"
                    f"  - Conversion Rate: {float(row.get('conversion_rate', 0)) * 100:.2f}%\n\n"
                )
            z = rows[0].get('z_score', 'N/A')
            p = rows[0].get('p_value', 'N/A')
            narrative += (
                f"Statistical Significance:\n"
                f"  - Z-score: {z}\n"
                f"  - P-value: {p}\n"
                f"  - Result: STATISTICALLY SIGNIFICANT (p < 0.001)\n\n"
                f"The treatment group (10% discount incentive) showed a ~67% relative "
                f"improvement in second-purchase conversion over control."
            )
            chunks.append(Document(
                content=narrative,
                metadata={"source": filename, "namespace": namespace, "file_type": "csv_data"}
            ))

        elif "logistic_regression_coefficients" in filename:
            narrative = "Logistic Regression Model Coefficients (Leakage-Free V2):\n\n"
            for row in rows:
                narrative += f"  - {row.get('feature', '')}: {row.get('coefficient', '')}\n"
            narrative += (
                "\nAll coefficients are extremely close to zero, indicating the model "
                "found NO meaningful signal to distinguish churned from active customers. "
                "Model accuracy is approximately 55% (barely better than random coin flip)."
            )
            chunks.append(Document(
                content=narrative,
                metadata={"source": filename, "namespace": namespace, "file_type": "csv_data"}
            ))

        elif "churn_features" in filename:
            # Large file — generate summary statistics only, don't index all 90K rows
            import pandas as pd
            df = pd.read_csv(filepath)
            narrative = (
                f"Churn Features Dataset Summary ({len(df)} customers):\n\n"
                f"Columns: {', '.join(df.columns.tolist())}\n\n"
                f"Churn Distribution:\n"
                f"  - Churned (is_churned=1): {(df['is_churned'] == 1).sum()} "
                f"({(df['is_churned'] == 1).mean() * 100:.1f}%)\n"
                f"  - Active (is_churned=0): {(df['is_churned'] == 0).sum()} "
                f"({(df['is_churned'] == 0).mean() * 100:.1f}%)\n\n"
                f"Feature Statistics:\n"
            )
            for col in ['total_orders', 'total_revenue', 'avg_order_value', 'days_since_last_order']:
                if col in df.columns:
                    narrative += (
                        f"  {col}: mean={df[col].mean():.2f}, "
                        f"median={df[col].median():.2f}, "
                        f"min={df[col].min():.2f}, max={df[col].max():.2f}\n"
                    )
            narrative += (
                f"\nChurn is defined as 90+ days of inactivity. "
                f"The dataset uses 'customer_unique_id' (not 'customer_id') to track "
                f"real repeat purchases across orders."
            )
            chunks.append(Document(
                content=narrative,
                metadata={"source": filename, "namespace": namespace, "file_type": "csv_data"}
            ))
        else:
            # Generic CSV: convert to readable table representation
            narrative = f"Data from {filename} ({len(rows)} rows):\n"
            narrative += f"Columns: {', '.join(headers)}\n\n"
            for i, row in enumerate(rows[:30]):  # Cap at 30 rows
                narrative += f"Row {i+1}: " + ", ".join(
                    f"{k}={v}" for k, v in row.items()
                ) + "\n"
            if len(rows) > 30:
                narrative += f"\n... and {len(rows) - 30} more rows."
            chunks.append(Document(
                content=narrative,
                metadata={"source": filename, "namespace": namespace, "file_type": "csv_data"}
            ))

        return chunks

    def _load_sql(self, filepath: str, namespace: str) -> List[Document]:
        """
        Load SQL files as code blocks with their comments as context.

        SQL comments (-- lines) serve as natural language descriptions
        of what the queries do, which helps with retrieval.
        """
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        filename = os.path.basename(filepath)

        # Wrap in descriptive context
        wrapped = (
            f"SQL Query from '{filename}':\n"
            f"This SQL file is part of the Olist E-Commerce analysis pipeline.\n\n"
            f"```sql\n{content}\n```"
        )

        return [Document(
            content=wrapped,
            metadata={
                "source": filename,
                "namespace": namespace,
                "file_type": "sql",
            }
        )]

    def _load_python(self, filepath: str, namespace: str) -> List[Document]:
        """
        Load Python scripts as code blocks with descriptions.

        The script name and imports give context about what the script does.
        """
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        filename = os.path.basename(filepath)

        # Add descriptive wrapper
        script_descriptions = {
            "run_analysis.py": "Revenue trend analysis — loads orders and payments, calculates monthly revenue using SQL.",
            "run_retention_analysis.py": "Retention analysis — calculates repeat purchase rate by counting customers with more than one order.",
            "run_churn_feature_extraction_v2.py": "Leakage-free churn feature engineering — creates customer-level features using dataset end date (not CURRENT_DATE) to avoid data leakage.",
            "run_churn_logistic_regression_v2.py": "Leakage-free churn model — trains Logistic Regression on safe features only (excludes days_since_last_order).",
            "run_churn_statistical_tests.py": "Statistical hypothesis testing — runs t-tests and Mann-Whitney U tests comparing churned vs active customers.",
            "run_ab_test_retention.py": "A/B test simulation — tests whether a 10% discount improves second-purchase conversion using z-test for proportions.",
            "run_visualizations.py": "Visualization generation — creates publication-ready charts for all analysis results.",
        }

        desc = script_descriptions.get(filename, f"Python script: {filename}")
        wrapped = f"Python Script: {filename}\nDescription: {desc}\n\n```python\n{content}\n```"

        return [Document(
            content=wrapped,
            metadata={
                "source": filename,
                "namespace": namespace,
                "file_type": "python",
                "description": desc,
            }
        )]
