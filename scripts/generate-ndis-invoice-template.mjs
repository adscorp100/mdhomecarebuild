import { Document, Packer, Paragraph, Table, TableRow, TableCell, TextRun, WidthType, BorderStyle, AlignmentType, TableLayoutType } from 'docx';
import * as fs from 'fs';
import * as path from 'path';

// Full page width in twips (A4 is ~9026 twips wide minus margins)
const PAGE_WIDTH = 9026;

// Create the NDIS Invoice Template
const doc = new Document({
  sections: [
    {
      properties: {
        page: {
          margin: {
            top: 720,
            right: 720,
            bottom: 720,
            left: 720,
          },
        },
      },
      children: [
        // Header - Provider Details
        new Paragraph({
          children: [
            new TextRun({
              text: "TAX INVOICE",
              bold: true,
              size: 48,
              color: "1a5276",
            }),
          ],
          alignment: AlignmentType.CENTER,
          spacing: { after: 400 },
        }),

        // Provider Information Section
        new Paragraph({
          children: [
            new TextRun({
              text: "[Your Business Name / ABN]",
              bold: true,
              size: 28,
              color: "2c3e50",
            }),
          ],
          spacing: { after: 100 },
        }),
        new Paragraph({
          children: [
            new TextRun({ text: "ABN: [Your ABN Number]", size: 22 }),
          ],
          spacing: { after: 50 },
        }),
        new Paragraph({
          children: [
            new TextRun({ text: "Address: [Your Business Address]", size: 22 }),
          ],
          spacing: { after: 50 },
        }),
        new Paragraph({
          children: [
            new TextRun({ text: "Phone: [Your Phone Number]", size: 22 }),
          ],
          spacing: { after: 50 },
        }),
        new Paragraph({
          children: [
            new TextRun({ text: "Email: [Your Email Address]", size: 22 }),
          ],
          spacing: { after: 50 },
        }),
        new Paragraph({
          children: [
            new TextRun({ text: "NDIS Registration Number: [Your NDIS Reg No.]", size: 22 }),
          ],
          spacing: { after: 400 },
        }),

        // Invoice Details Table
        new Table({
          width: { size: PAGE_WIDTH, type: WidthType.DXA },
          layout: TableLayoutType.FIXED,
          columnWidths: [2256, 2256, 2256, 2258],
          rows: [
            new TableRow({
              children: [
                new TableCell({
                  children: [new Paragraph({ children: [new TextRun({ text: "Invoice Number:", bold: true, size: 22 })] })],
                  width: { size: 2256, type: WidthType.DXA },
                  shading: { fill: "ecf0f1" },
                }),
                new TableCell({
                  children: [new Paragraph({ children: [new TextRun({ text: "[INV-0001]", size: 22 })] })],
                  width: { size: 2256, type: WidthType.DXA },
                }),
                new TableCell({
                  children: [new Paragraph({ children: [new TextRun({ text: "Invoice Date:", bold: true, size: 22 })] })],
                  width: { size: 2256, type: WidthType.DXA },
                  shading: { fill: "ecf0f1" },
                }),
                new TableCell({
                  children: [new Paragraph({ children: [new TextRun({ text: "[DD/MM/YYYY]", size: 22 })] })],
                  width: { size: 2258, type: WidthType.DXA },
                }),
              ],
            }),
            new TableRow({
              children: [
                new TableCell({
                  children: [new Paragraph({ children: [new TextRun({ text: "Service Period:", bold: true, size: 22 })] })],
                  width: { size: 2256, type: WidthType.DXA },
                  shading: { fill: "ecf0f1" },
                }),
                new TableCell({
                  children: [new Paragraph({ children: [new TextRun({ text: "[Start Date] to [End Date]", size: 22 })] })],
                  width: { size: 2256, type: WidthType.DXA },
                }),
                new TableCell({
                  children: [new Paragraph({ children: [new TextRun({ text: "Payment Due:", bold: true, size: 22 })] })],
                  width: { size: 2256, type: WidthType.DXA },
                  shading: { fill: "ecf0f1" },
                }),
                new TableCell({
                  children: [new Paragraph({ children: [new TextRun({ text: "[DD/MM/YYYY]", size: 22 })] })],
                  width: { size: 2258, type: WidthType.DXA },
                }),
              ],
            }),
          ],
        }),

        new Paragraph({ spacing: { after: 300 } }),

        // Participant Details Section
        new Paragraph({
          children: [
            new TextRun({
              text: "PARTICIPANT DETAILS",
              bold: true,
              size: 24,
              color: "1a5276",
            }),
          ],
          spacing: { after: 200, before: 200 },
          border: { bottom: { color: "1a5276", size: 1, style: BorderStyle.SINGLE } },
        }),

        new Table({
          width: { size: PAGE_WIDTH, type: WidthType.DXA },
          layout: TableLayoutType.FIXED,
          columnWidths: [2700, 6326],
          rows: [
            new TableRow({
              children: [
                new TableCell({
                  children: [new Paragraph({ children: [new TextRun({ text: "Participant Name:", bold: true, size: 22 })] })],
                  width: { size: 2700, type: WidthType.DXA },
                  shading: { fill: "ecf0f1" },
                }),
                new TableCell({
                  children: [new Paragraph({ children: [new TextRun({ text: "[Participant Full Name]", size: 22 })] })],
                  width: { size: 6326, type: WidthType.DXA },
                }),
              ],
            }),
            new TableRow({
              children: [
                new TableCell({
                  children: [new Paragraph({ children: [new TextRun({ text: "NDIS Number:", bold: true, size: 22 })] })],
                  width: { size: 2700, type: WidthType.DXA },
                  shading: { fill: "ecf0f1" },
                }),
                new TableCell({
                  children: [new Paragraph({ children: [new TextRun({ text: "[Participant NDIS Number]", size: 22 })] })],
                  width: { size: 6326, type: WidthType.DXA },
                }),
              ],
            }),
            new TableRow({
              children: [
                new TableCell({
                  children: [new Paragraph({ children: [new TextRun({ text: "Date of Birth:", bold: true, size: 22 })] })],
                  width: { size: 2700, type: WidthType.DXA },
                  shading: { fill: "ecf0f1" },
                }),
                new TableCell({
                  children: [new Paragraph({ children: [new TextRun({ text: "[DD/MM/YYYY]", size: 22 })] })],
                  width: { size: 6326, type: WidthType.DXA },
                }),
              ],
            }),
            new TableRow({
              children: [
                new TableCell({
                  children: [new Paragraph({ children: [new TextRun({ text: "Address:", bold: true, size: 22 })] })],
                  width: { size: 2700, type: WidthType.DXA },
                  shading: { fill: "ecf0f1" },
                }),
                new TableCell({
                  children: [new Paragraph({ children: [new TextRun({ text: "[Participant Address]", size: 22 })] })],
                  width: { size: 6326, type: WidthType.DXA },
                }),
              ],
            }),
            new TableRow({
              children: [
                new TableCell({
                  children: [new Paragraph({ children: [new TextRun({ text: "Plan Manager:", bold: true, size: 22 })] })],
                  width: { size: 2700, type: WidthType.DXA },
                  shading: { fill: "ecf0f1" },
                }),
                new TableCell({
                  children: [new Paragraph({ children: [new TextRun({ text: "[Plan Manager Name & Email (if applicable)]", size: 22 })] })],
                  width: { size: 6326, type: WidthType.DXA },
                }),
              ],
            }),
          ],
        }),

        new Paragraph({ spacing: { after: 300 } }),

        // Services Provided Section
        new Paragraph({
          children: [
            new TextRun({
              text: "SERVICES PROVIDED",
              bold: true,
              size: 24,
              color: "1a5276",
            }),
          ],
          spacing: { after: 200, before: 200 },
          border: { bottom: { color: "1a5276", size: 1, style: BorderStyle.SINGLE } },
        }),

        // Services Table - 6 columns
        new Table({
          width: { size: PAGE_WIDTH, type: WidthType.DXA },
          layout: TableLayoutType.FIXED,
          columnWidths: [1100, 1800, 2800, 1100, 1100, 1126],
          rows: [
            // Header Row
            new TableRow({
              children: [
                new TableCell({
                  children: [new Paragraph({ children: [new TextRun({ text: "Date", bold: true, size: 20, color: "ffffff" })] })],
                  shading: { fill: "1a5276" },
                  width: { size: 1100, type: WidthType.DXA },
                }),
                new TableCell({
                  children: [new Paragraph({ children: [new TextRun({ text: "Support Item No.", bold: true, size: 20, color: "ffffff" })] })],
                  shading: { fill: "1a5276" },
                  width: { size: 1800, type: WidthType.DXA },
                }),
                new TableCell({
                  children: [new Paragraph({ children: [new TextRun({ text: "Description", bold: true, size: 20, color: "ffffff" })] })],
                  shading: { fill: "1a5276" },
                  width: { size: 2800, type: WidthType.DXA },
                }),
                new TableCell({
                  children: [new Paragraph({ children: [new TextRun({ text: "Qty/Hrs", bold: true, size: 20, color: "ffffff" })] })],
                  shading: { fill: "1a5276" },
                  width: { size: 1100, type: WidthType.DXA },
                }),
                new TableCell({
                  children: [new Paragraph({ children: [new TextRun({ text: "Rate", bold: true, size: 20, color: "ffffff" })] })],
                  shading: { fill: "1a5276" },
                  width: { size: 1100, type: WidthType.DXA },
                }),
                new TableCell({
                  children: [new Paragraph({ children: [new TextRun({ text: "Amount", bold: true, size: 20, color: "ffffff" })] })],
                  shading: { fill: "1a5276" },
                  width: { size: 1126, type: WidthType.DXA },
                }),
              ],
            }),
            // Example Row 1
            new TableRow({
              children: [
                new TableCell({ children: [new Paragraph({ children: [new TextRun({ text: "[Date]", size: 20 })] })], width: { size: 1100, type: WidthType.DXA } }),
                new TableCell({ children: [new Paragraph({ children: [new TextRun({ text: "01_011_0107_1_1", size: 18 })] })], width: { size: 1800, type: WidthType.DXA } }),
                new TableCell({ children: [new Paragraph({ children: [new TextRun({ text: "Assistance with Daily Life - Standard", size: 20 })] })], width: { size: 2800, type: WidthType.DXA } }),
                new TableCell({ children: [new Paragraph({ children: [new TextRun({ text: "[Hours]", size: 20 })] })], width: { size: 1100, type: WidthType.DXA } }),
                new TableCell({ children: [new Paragraph({ children: [new TextRun({ text: "$[Rate]", size: 20 })] })], width: { size: 1100, type: WidthType.DXA } }),
                new TableCell({ children: [new Paragraph({ children: [new TextRun({ text: "$[Amount]", size: 20 })] })], width: { size: 1126, type: WidthType.DXA } }),
              ],
            }),
            // Example Row 2
            new TableRow({
              children: [
                new TableCell({ children: [new Paragraph({ children: [new TextRun({ text: "[Date]", size: 20 })] })], width: { size: 1100, type: WidthType.DXA } }),
                new TableCell({ children: [new Paragraph({ children: [new TextRun({ text: "04_104_0125_6_1", size: 18 })] })], width: { size: 1800, type: WidthType.DXA } }),
                new TableCell({ children: [new Paragraph({ children: [new TextRun({ text: "Community Participation - Weekday", size: 20 })] })], width: { size: 2800, type: WidthType.DXA } }),
                new TableCell({ children: [new Paragraph({ children: [new TextRun({ text: "[Hours]", size: 20 })] })], width: { size: 1100, type: WidthType.DXA } }),
                new TableCell({ children: [new Paragraph({ children: [new TextRun({ text: "$[Rate]", size: 20 })] })], width: { size: 1100, type: WidthType.DXA } }),
                new TableCell({ children: [new Paragraph({ children: [new TextRun({ text: "$[Amount]", size: 20 })] })], width: { size: 1126, type: WidthType.DXA } }),
              ],
            }),
            // Example Row 3
            new TableRow({
              children: [
                new TableCell({ children: [new Paragraph({ children: [new TextRun({ text: "[Date]", size: 20 })] })], width: { size: 1100, type: WidthType.DXA } }),
                new TableCell({ children: [new Paragraph({ children: [new TextRun({ text: "15_037_0117_1_3", size: 18 })] })], width: { size: 1800, type: WidthType.DXA } }),
                new TableCell({ children: [new Paragraph({ children: [new TextRun({ text: "Provider Travel - Non-Labour Costs", size: 20 })] })], width: { size: 2800, type: WidthType.DXA } }),
                new TableCell({ children: [new Paragraph({ children: [new TextRun({ text: "[km]", size: 20 })] })], width: { size: 1100, type: WidthType.DXA } }),
                new TableCell({ children: [new Paragraph({ children: [new TextRun({ text: "$[Rate]", size: 20 })] })], width: { size: 1100, type: WidthType.DXA } }),
                new TableCell({ children: [new Paragraph({ children: [new TextRun({ text: "$[Amount]", size: 20 })] })], width: { size: 1126, type: WidthType.DXA } }),
              ],
            }),
            // Empty rows for additional entries
            ...Array(5).fill(null).map(() =>
              new TableRow({
                children: [
                  new TableCell({ children: [new Paragraph({ children: [new TextRun({ text: "", size: 20 })] })], width: { size: 1100, type: WidthType.DXA } }),
                  new TableCell({ children: [new Paragraph({ children: [new TextRun({ text: "", size: 20 })] })], width: { size: 1800, type: WidthType.DXA } }),
                  new TableCell({ children: [new Paragraph({ children: [new TextRun({ text: "", size: 20 })] })], width: { size: 2800, type: WidthType.DXA } }),
                  new TableCell({ children: [new Paragraph({ children: [new TextRun({ text: "", size: 20 })] })], width: { size: 1100, type: WidthType.DXA } }),
                  new TableCell({ children: [new Paragraph({ children: [new TextRun({ text: "", size: 20 })] })], width: { size: 1100, type: WidthType.DXA } }),
                  new TableCell({ children: [new Paragraph({ children: [new TextRun({ text: "", size: 20 })] })], width: { size: 1126, type: WidthType.DXA } }),
                ],
              })
            ),
          ],
        }),

        new Paragraph({ spacing: { after: 300 } }),

        // Totals Section - Right aligned
        new Table({
          width: { size: PAGE_WIDTH, type: WidthType.DXA },
          layout: TableLayoutType.FIXED,
          columnWidths: [5500, 2000, 1526],
          rows: [
            new TableRow({
              children: [
                new TableCell({
                  children: [new Paragraph({ children: [] })],
                  width: { size: 5500, type: WidthType.DXA },
                  borders: { top: { size: 0, style: BorderStyle.NONE }, bottom: { size: 0, style: BorderStyle.NONE }, left: { size: 0, style: BorderStyle.NONE }, right: { size: 0, style: BorderStyle.NONE } },
                }),
                new TableCell({
                  children: [new Paragraph({ children: [new TextRun({ text: "Subtotal:", bold: true, size: 22 })], alignment: AlignmentType.RIGHT })],
                  width: { size: 2000, type: WidthType.DXA },
                  shading: { fill: "ecf0f1" },
                }),
                new TableCell({
                  children: [new Paragraph({ children: [new TextRun({ text: "$[Subtotal]", size: 22 })], alignment: AlignmentType.RIGHT })],
                  width: { size: 1526, type: WidthType.DXA },
                }),
              ],
            }),
            new TableRow({
              children: [
                new TableCell({
                  children: [new Paragraph({ children: [] })],
                  width: { size: 5500, type: WidthType.DXA },
                  borders: { top: { size: 0, style: BorderStyle.NONE }, bottom: { size: 0, style: BorderStyle.NONE }, left: { size: 0, style: BorderStyle.NONE }, right: { size: 0, style: BorderStyle.NONE } },
                }),
                new TableCell({
                  children: [new Paragraph({ children: [new TextRun({ text: "GST (if applicable):", bold: true, size: 22 })], alignment: AlignmentType.RIGHT })],
                  width: { size: 2000, type: WidthType.DXA },
                  shading: { fill: "ecf0f1" },
                }),
                new TableCell({
                  children: [new Paragraph({ children: [new TextRun({ text: "$[GST]", size: 22 })], alignment: AlignmentType.RIGHT })],
                  width: { size: 1526, type: WidthType.DXA },
                }),
              ],
            }),
            new TableRow({
              children: [
                new TableCell({
                  children: [new Paragraph({ children: [] })],
                  width: { size: 5500, type: WidthType.DXA },
                  borders: { top: { size: 0, style: BorderStyle.NONE }, bottom: { size: 0, style: BorderStyle.NONE }, left: { size: 0, style: BorderStyle.NONE }, right: { size: 0, style: BorderStyle.NONE } },
                }),
                new TableCell({
                  children: [new Paragraph({ children: [new TextRun({ text: "TOTAL DUE:", bold: true, size: 24, color: "1a5276" })], alignment: AlignmentType.RIGHT })],
                  width: { size: 2000, type: WidthType.DXA },
                  shading: { fill: "d5e8d4" },
                }),
                new TableCell({
                  children: [new Paragraph({ children: [new TextRun({ text: "$[Total]", bold: true, size: 24, color: "1a5276" })], alignment: AlignmentType.RIGHT })],
                  width: { size: 1526, type: WidthType.DXA },
                  shading: { fill: "d5e8d4" },
                }),
              ],
            }),
          ],
        }),

        new Paragraph({ spacing: { after: 400 } }),

        // Payment Details Section
        new Paragraph({
          children: [
            new TextRun({
              text: "PAYMENT DETAILS",
              bold: true,
              size: 24,
              color: "1a5276",
            }),
          ],
          spacing: { after: 200, before: 200 },
          border: { bottom: { color: "1a5276", size: 1, style: BorderStyle.SINGLE } },
        }),

        new Table({
          width: { size: PAGE_WIDTH, type: WidthType.DXA },
          layout: TableLayoutType.FIXED,
          columnWidths: [2700, 6326],
          rows: [
            new TableRow({
              children: [
                new TableCell({
                  children: [new Paragraph({ children: [new TextRun({ text: "Bank Name:", bold: true, size: 22 })] })],
                  width: { size: 2700, type: WidthType.DXA },
                  shading: { fill: "ecf0f1" },
                }),
                new TableCell({
                  children: [new Paragraph({ children: [new TextRun({ text: "[Your Bank Name]", size: 22 })] })],
                  width: { size: 6326, type: WidthType.DXA },
                }),
              ],
            }),
            new TableRow({
              children: [
                new TableCell({
                  children: [new Paragraph({ children: [new TextRun({ text: "Account Name:", bold: true, size: 22 })] })],
                  width: { size: 2700, type: WidthType.DXA },
                  shading: { fill: "ecf0f1" },
                }),
                new TableCell({
                  children: [new Paragraph({ children: [new TextRun({ text: "[Your Account Name]", size: 22 })] })],
                  width: { size: 6326, type: WidthType.DXA },
                }),
              ],
            }),
            new TableRow({
              children: [
                new TableCell({
                  children: [new Paragraph({ children: [new TextRun({ text: "BSB:", bold: true, size: 22 })] })],
                  width: { size: 2700, type: WidthType.DXA },
                  shading: { fill: "ecf0f1" },
                }),
                new TableCell({
                  children: [new Paragraph({ children: [new TextRun({ text: "[XXX-XXX]", size: 22 })] })],
                  width: { size: 6326, type: WidthType.DXA },
                }),
              ],
            }),
            new TableRow({
              children: [
                new TableCell({
                  children: [new Paragraph({ children: [new TextRun({ text: "Account Number:", bold: true, size: 22 })] })],
                  width: { size: 2700, type: WidthType.DXA },
                  shading: { fill: "ecf0f1" },
                }),
                new TableCell({
                  children: [new Paragraph({ children: [new TextRun({ text: "[XXXXXXXX]", size: 22 })] })],
                  width: { size: 6326, type: WidthType.DXA },
                }),
              ],
            }),
            new TableRow({
              children: [
                new TableCell({
                  children: [new Paragraph({ children: [new TextRun({ text: "Payment Reference:", bold: true, size: 22 })] })],
                  width: { size: 2700, type: WidthType.DXA },
                  shading: { fill: "ecf0f1" },
                }),
                new TableCell({
                  children: [new Paragraph({ children: [new TextRun({ text: "[Invoice Number + Participant Name]", size: 22 })] })],
                  width: { size: 6326, type: WidthType.DXA },
                }),
              ],
            }),
          ],
        }),

        new Paragraph({ spacing: { after: 400 } }),

        // Notes Section
        new Paragraph({
          children: [
            new TextRun({
              text: "NOTES & TERMS",
              bold: true,
              size: 24,
              color: "1a5276",
            }),
          ],
          spacing: { after: 200 },
          border: { bottom: { color: "1a5276", size: 1, style: BorderStyle.SINGLE } },
        }),

        new Paragraph({
          children: [
            new TextRun({ text: "• ", size: 20 }),
            new TextRun({ text: "All rates comply with the NDIS Pricing Arrangements and Price Limits 2024-25", size: 20 }),
          ],
          spacing: { after: 100 },
        }),
        new Paragraph({
          children: [
            new TextRun({ text: "• ", size: 20 }),
            new TextRun({ text: "Payment is due within 14 days of invoice date (or as per service agreement)", size: 20 }),
          ],
          spacing: { after: 100 },
        }),
        new Paragraph({
          children: [
            new TextRun({ text: "• ", size: 20 }),
            new TextRun({ text: "For NDIA-managed participants: Claims submitted directly to the NDIA portal", size: 20 }),
          ],
          spacing: { after: 100 },
        }),
        new Paragraph({
          children: [
            new TextRun({ text: "• ", size: 20 }),
            new TextRun({ text: "For plan-managed participants: Please forward to your plan manager", size: 20 }),
          ],
          spacing: { after: 100 },
        }),
        new Paragraph({
          children: [
            new TextRun({ text: "• ", size: 20 }),
            new TextRun({ text: "Service records and progress notes available upon request", size: 20 }),
          ],
          spacing: { after: 200 },
        }),

        // Footer
        new Paragraph({
          children: [
            new TextRun({
              text: "Thank you for choosing our services. For any queries regarding this invoice, please contact us.",
              italics: true,
              size: 20,
              color: "7f8c8d",
            }),
          ],
          alignment: AlignmentType.CENTER,
          spacing: { before: 400 },
        }),

      ],
    },
  ],
});

// Generate and save the document
const outputPath = path.join(process.cwd(), 'public', 'downloads', 'ndis-invoice-template-2025.docx');

Packer.toBuffer(doc).then((buffer) => {
  fs.writeFileSync(outputPath, buffer);
  console.log(`NDIS Invoice Template saved to: ${outputPath}`);
});
