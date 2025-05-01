"""
Project Homepage: https://github.com/AutoBotSolutions/Aurora.git
License: MIT (or choose your open-source license)
Maintainer: G.O.D Framework Team
Contact: support@autobotsolutions.com   
"""

import logging
from fpdf import FPDF


class AdvancedReporting:
    """
    Provides methods to generate PDF reports summarizing pipeline metrics and insights,
    and to configure logging for the report generation process.

    This class is designed to handle the creation of professional-quality PDF reports
    based on given pipeline data. Additionally, it offers a utility to setup logging
    for monitoring and debugging purposes.

    :ivar default_font: Default font used for the PDF reports.
    :type default_font: str
    :ivar default_font_size: Default size of the font used in PDF reports.
    :type default_font_size: int
    :ivar log_level: Default logging level for report generation process.
    :type log_level: int
    """

    @staticmethod
    def generate_pdf_report(report_data, output_path):
        """
        Generates a PDF report summarizing pipeline metrics and insights.

        :param report_data: Dictionary containing metrics, charts, or summaries.
        :param output_path: String, the path where the PDF report will be saved.
        """
        logging.info("Starting PDF report generation...")
        try:
            # Initialize the PDF object
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)

            # Add title
            pdf.cell(200, 10, txt="Pipeline Report", ln=True, align="C")
            pdf.ln(10)  # Add a line break

            # Fill the report data into PDF
            for key, value in report_data.items():
                if isinstance(value, dict):
                    # Handle nested dictionaries by flattening them
                    pdf.cell(200, 10, txt=f"{key}:", ln=True, align="L")
                    for sub_key, sub_value in value.items():
                        pdf.cell(200, 10, txt=f"    {sub_key}: {sub_value}", ln=True, align="L")
                else:
                    pdf.cell(200, 10, txt=f"{key}: {value}", ln=True, align="L")

            # Save the PDF to the specified output path
            pdf.output(output_path)
            logging.info(f"PDF report successfully saved at: {output_path}")
        except Exception as e:
            logging.error(f"Failed to generate PDF report: {e}")
            raise

    @staticmethod
    def setup_logging(level=logging.INFO, log_file=None):
        """
        Configures logging for the report generation process.

        :param level: Logging level (default: logging.INFO).
        :param log_file: Optional, file path to store logs. Logs to console if not specified.
        """
        handlers = [logging.StreamHandler()]
        if log_file:
            handlers.append(logging.FileHandler(log_file))

        logging.basicConfig(
            level=level,
            format="%(asctime)s - %(levelname)s - %(message)s",
            handlers=handlers,
        )


if __name__ == "__main__":
    # Setup logging for the script
    AdvancedReporting.setup_logging(level=logging.DEBUG)

    logging.info("Advanced Reporting Script Started...")

    # Example Usage: Sample report data
    example_report_data = {
        "Model": "Random Forest",
        "Accuracy": "87%",
        "Precision": "85%",
        "Recall": "81%",
        "Training Summary": {
            "Training Time": "15 minutes",
            "Training Data": "Dataset-X",
        },
        "Final Comments": "The performance is satisfactory, with opportunities for improvement in recall."
    }

    # Generating the report
    output_report_path = "advanced_pipeline_report.pdf"
    AdvancedReporting.generate_pdf_report(example_report_data, output_report_path)
