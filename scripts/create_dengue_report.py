from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    HRFlowable,
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


OUTPUT_PATH = Path(__file__).resolve().parents[1] / "output" / "pdf" / "dengue_fever_project_report.pdf"

NAVY = colors.HexColor("#14364A")
TEAL = colors.HexColor("#1C7A7A")
CORAL = colors.HexColor("#B64C48")
PALE_TEAL = colors.HexColor("#E7F3F2")
PALE_CORAL = colors.HexColor("#FAECE9")
INK = colors.HexColor("#1E2A33")
MUTED = colors.HexColor("#5E6B73")
RULE = colors.HexColor("#C9D9D9")


def citation(*numbers):
    return " <super>[" + ", ".join(str(number) for number in numbers) + "]</super>"


def first_page(canvas, document):
    canvas.saveState()
    width, height = A4
    canvas.setFillColor(NAVY)
    canvas.rect(0, 0, width, height, fill=1, stroke=0)
    canvas.setFillColor(TEAL)
    canvas.rect(0, height - 4.0 * cm, width, 4.0 * cm, fill=1, stroke=0)
    canvas.setFillColor(CORAL)
    canvas.circle(width - 2.0 * cm, height - 1.3 * cm, 1.2 * cm, fill=1, stroke=0)
    canvas.setStrokeColor(colors.Color(1, 1, 1, alpha=0.22))
    canvas.setLineWidth(1.2)
    canvas.circle(width - 2.0 * cm, height - 1.3 * cm, 2.1 * cm, fill=0, stroke=1)
    canvas.setFillColor(colors.Color(1, 1, 1, alpha=0.12))
    canvas.circle(2.0 * cm, 2.2 * cm, 1.1 * cm, fill=1, stroke=0)
    canvas.circle(3.5 * cm, 1.2 * cm, 0.55 * cm, fill=1, stroke=0)
    canvas.restoreState()


def later_pages(canvas, document):
    canvas.saveState()
    width, height = A4
    canvas.setStrokeColor(RULE)
    canvas.setLineWidth(0.5)
    canvas.line(1.8 * cm, height - 1.55 * cm, width - 1.8 * cm, height - 1.55 * cm)
    canvas.setFont("Helvetica-Bold", 8)
    canvas.setFillColor(TEAL)
    canvas.drawString(1.8 * cm, height - 1.18 * cm, "DENGUE FEVER")
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(MUTED)
    canvas.drawRightString(width - 1.8 * cm, height - 1.18 * cm, "Project Report | 2026")
    canvas.setStrokeColor(RULE)
    canvas.line(1.8 * cm, 1.3 * cm, width - 1.8 * cm, 1.3 * cm)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(MUTED)
    canvas.drawString(1.8 * cm, 0.92 * cm, "Comprehensive clinical and public health review")
    canvas.drawRightString(width - 1.8 * cm, 0.92 * cm, f"Page {document.page}")
    canvas.restoreState()


def build_styles():
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name="CoverKicker", parent=styles["Normal"], fontName="Helvetica-Bold",
        fontSize=11, leading=14, textColor=colors.white, alignment=TA_CENTER,
        spaceAfter=12,
    ))
    styles.add(ParagraphStyle(
        name="CoverTitle", parent=styles["Title"], fontName="Helvetica-Bold",
        fontSize=34, leading=40, textColor=colors.white, alignment=TA_CENTER,
        spaceAfter=12,
    ))
    styles.add(ParagraphStyle(
        name="CoverSub", parent=styles["Normal"], fontName="Helvetica",
        fontSize=14, leading=20, textColor=colors.HexColor("#D6F0EF"), alignment=TA_CENTER,
        spaceAfter=30,
    ))
    styles.add(ParagraphStyle(
        name="CoverMeta", parent=styles["Normal"], fontName="Helvetica",
        fontSize=10.5, leading=16, textColor=colors.white, alignment=TA_CENTER,
    ))
    styles.add(ParagraphStyle(
        name="ReportTitle", parent=styles["Title"], fontName="Helvetica-Bold",
        fontSize=24, leading=29, textColor=NAVY, alignment=TA_LEFT, spaceAfter=12,
    ))
    styles.add(ParagraphStyle(
        name="Section", parent=styles["Heading1"], fontName="Helvetica-Bold",
        fontSize=16, leading=20, textColor=NAVY, spaceBefore=17, spaceAfter=9,
        keepWithNext=True,
    ))
    styles.add(ParagraphStyle(
        name="Subsection", parent=styles["Heading2"], fontName="Helvetica-Bold",
        fontSize=11.5, leading=15, textColor=TEAL, spaceBefore=11, spaceAfter=5,
        keepWithNext=True,
    ))
    styles.add(ParagraphStyle(
        name="Body", parent=styles["BodyText"], fontName="Helvetica", fontSize=9.7,
        leading=14.2, textColor=INK, alignment=TA_JUSTIFY, spaceAfter=8,
    ))
    styles.add(ParagraphStyle(
        name="Contents", parent=styles["BodyText"], fontName="Helvetica", fontSize=9.8,
        leading=15, textColor=INK, leftIndent=4, spaceAfter=0,
    ))
    styles.add(ParagraphStyle(
        name="TableText", parent=styles["BodyText"], fontName="Helvetica", fontSize=8.5,
        leading=11.3, textColor=INK,
    ))
    styles.add(ParagraphStyle(
        name="TableHead", parent=styles["BodyText"], fontName="Helvetica-Bold", fontSize=8.4,
        leading=10.5, textColor=colors.white, alignment=TA_LEFT,
    ))
    styles.add(ParagraphStyle(
        name="Reference", parent=styles["BodyText"], fontName="Helvetica", fontSize=8.6,
        leading=12.2, textColor=INK, leftIndent=0, firstLineIndent=0, spaceAfter=5,
    ))
    styles.add(ParagraphStyle(
        name="SmallNote", parent=styles["BodyText"], fontName="Helvetica-Oblique", fontSize=8.5,
        leading=11.5, textColor=MUTED, spaceAfter=8,
    ))
    return styles


def p(text, style):
    return Paragraph(text, style)


def info_box(title, text, styles):
    content = [[p(f"<b>{title}</b><br/>{text}", styles["TableText"])]]
    box = Table(content, colWidths=[16.2 * cm])
    box.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), PALE_TEAL),
        ("BOX", (0, 0), (-1, -1), 0.7, TEAL),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    return KeepTogether([box, Spacer(1, 10)])


def data_table(headers, rows, widths, styles):
    data = [[p(header, styles["TableHead"]) for header in headers]]
    data.extend([[p(cell, styles["TableText"]) for cell in row] for row in rows])
    table = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.35, RULE),
        ("BACKGROUND", (0, 1), (-1, -1), colors.white),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F5F9F9")]),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    return KeepTogether([table, Spacer(1, 11)])


def add_section(story, title, styles):
    story.append(p(title, styles["Section"]))
    story.append(HRFlowable(width="100%", thickness=0.8, color=RULE, spaceAfter=7))


def add_subsection(story, title, paragraphs, styles):
    story.append(p(title, styles["Subsection"]))
    for paragraph in paragraphs:
        story.append(p(paragraph, styles["Body"]))


def make_story(styles):
    story = []

    story.extend([
        Spacer(1, 6.3 * cm),
        p("PROJECT REPORT", styles["CoverKicker"]),
        p("DENGUE FEVER", styles["CoverTitle"]),
        p("A Comprehensive Clinical, Epidemiological, and Public Health Review", styles["CoverSub"]),
        HRFlowable(width="42%", thickness=1.1, color=colors.HexColor("#A7D8D5"), hAlign="CENTER", spaceAfter=18),
        p("Prepared for Academic Project Submission<br/>July 2026", styles["CoverMeta"]),
        Spacer(1, 0.55 * cm),
        p("This report uses current World Health Organization and Centers for Disease Control and Prevention guidance, supported by peer-reviewed literature.", styles["CoverMeta"]),
        PageBreak(),
    ])

    story.append(p("Report Contents", styles["ReportTitle"]))
    story.append(p("The report follows the requested project-report headings and summarizes accepted clinical and public-health evidence.", styles["SmallNote"]))
    contents = [
        "1. Introduction", "Definition of Rare Disease", "Background and Significance", "Disease Overview",
        "2. Epidemiology (Prevalence and Incidence)", "3. Etiology and Risk Factors", "Genetic Causes",
        "Environmental Factors", "Other Contributing Factors", "4. Pathophysiology", "Disease Mechanism",
        "Molecular and Cellular Changes", "5. Clinical Manifestations", "Signs and Symptoms", "Disease Progression",
        "6. Diagnosis", "Diagnostic Criteria", "Laboratory Tests", "Imaging Techniques", "Genetic Testing",
        "7. Treatment and Management", "Pharmacological Management", "Non-Pharmacological Management",
        "Supportive Care", "8. Challenges and Future Perspectives", "Challenges in Diagnosis and Treatment",
        "Future Research Directions", "Conclusion", "References",
    ]
    story.extend(p(item, styles["Contents"]) for item in contents)
    story.append(PageBreak())

    add_section(story, "1. Introduction", styles)
    add_subsection(story, "Definition of Rare Disease", [
        "Rare diseases are commonly defined in the United States as conditions affecting fewer than 200,000 people nationally, and in the European Union as those affecting no more than 1 in 2,000 people. Dengue fever does <b>not</b> meet either definition. It is a major mosquito-borne viral disease with widespread transmission in tropical and subtropical regions. The heading is nevertheless useful because it distinguishes a rare-disease framework from the population-level threat posed by dengue.",
        "Dengue may appear uncommon in non-endemic settings, where clinicians have less experience recognizing it and imported cases can be missed. Severe dengue is also relatively infrequent among all infections, but it is clinically important because plasma leakage, shock, severe bleeding, and organ impairment can develop rapidly. Early recognition therefore matters even where dengue is not routinely encountered." + citation(1, 4),
    ], styles)
    add_subsection(story, "Background and Significance", [
        "Dengue is caused by dengue virus (DENV), a flavivirus transmitted primarily by infected female <i>Aedes aegypti</i> mosquitoes; <i>Aedes albopictus</i> can contribute to transmission in some settings. Four antigenically distinct serotypes circulate (DENV-1 to DENV-4). Infection with one serotype usually produces long-lasting protection against that serotype but only temporary, partial protection against the others.",
        "Its public-health significance reflects explosive urban outbreaks, pressure on health services during seasonal epidemics, and the risk of fatal disease when warning signs are missed. Approximately half of the global population lives in areas at risk, and WHO estimates 100-400 million infections each year. Climate variability, unplanned urban growth, travel, trade, and expanding mosquito habitats all influence disease distribution." + citation(1, 5),
    ], styles)
    add_subsection(story, "Disease Overview", [
        "Dengue ranges from asymptomatic infection to an acute febrile illness and, in a minority, severe dengue. The illness is not simply a high fever: the phase around defervescence can mark a transition to capillary leak, intravascular volume depletion, shock, and organ injury. WHO clinical classification groups patients as dengue without warning signs, dengue with warning signs, or severe dengue.",
        "The disease is preventable chiefly through vector control and personal protection from mosquito bites. No broadly used, virus-specific antiviral treatment is available. Good outcomes depend on triage, serial assessment, judicious fluid management, and prompt escalation for warning signs or organ dysfunction." + citation(1, 3, 4),
    ], styles)
    story.append(info_box("Clinical emphasis", "Fever settling does not always mean recovery. The critical phase often begins near defervescence, so patients need clear return precautions and repeated assessment during this period.", styles))

    add_section(story, "2. Epidemiology (Prevalence and Incidence)", styles)
    add_subsection(story, "Global Pattern of Disease", [
        "Dengue is endemic in more than 100 countries and is concentrated in tropical and subtropical urban and semi-urban environments. Surveillance estimates are affected by asymptomatic infection, limited testing, inconsistent case definitions, and under-reporting. Modelling studies have estimated roughly 390 million DENV infections annually, with a substantially smaller fraction clinically apparent.",
        "Unlike chronic diseases, dengue is often described through incident symptomatic cases, outbreaks, hospitalization, and mortality rather than point prevalence. Transmission is seasonal in many settings, corresponding to rainfall, temperature, water storage practices, mosquito density, and local immunity. Large epidemics can occur when a new serotype or genotype reaches populations with limited immunity." + citation(1, 5, 13),
    ], styles)
    add_subsection(story, "Population Groups at Higher Risk", [
        "Severe disease risk is shaped by age, pregnancy, comorbid illness, viral factors, access to care, and previous DENV exposure. A second infection with a different serotype can increase the risk of severe dengue, although severe disease can also occur during a primary infection. Infants, older adults, pregnant people, and patients with chronic cardiometabolic, renal, hepatic, or hematologic conditions need careful monitoring.",
        "The burden includes outpatient visits, hospital admissions, lost school and work days, vector-control costs, and disruption during outbreaks. At the individual level, most symptomatic patients recover within one to two weeks, but the minority who progress to severe dengue require immediate hospital-level care." + citation(1, 3, 8),
    ], styles)
    story.append(data_table(
        ["Measure", "Interpretation for dengue"],
        [
            ["Annual infections", "WHO estimates approximately 100-400 million DENV infections worldwide each year; many are asymptomatic or mild."],
            ["Population at risk", "About half of the global population lives in areas at risk of dengue transmission."],
            ["Symptomatic illness", "Only a proportion of infections are clinically apparent; surveillance therefore underestimates total transmission."],
            ["Severe disease", "A small proportion of symptomatic cases progress, but severe dengue can become life-threatening within hours."],
        ], [4.3 * cm, 11.9 * cm], styles))

    add_section(story, "3. Etiology and Risk Factors", styles)
    add_subsection(story, "Genetic Causes", [
        "Dengue is an infectious disease rather than a monogenic disorder. Host genetic variation can, however, influence susceptibility to symptomatic disease, inflammatory responses, vascular permeability, and the likelihood of severe outcomes. Associations have been reported for variants in HLA loci and genes involved in innate immunity, cytokine signalling, Fc receptors, and viral entry. These findings are heterogeneous across ancestry groups and should not be interpreted as deterministic genetic tests.",
        "Viral genetics also matters. DENV serotypes and genotypes differ in fitness, transmissibility, and epidemic potential. The interaction among host immunity, viral lineage, and population-level immunity helps explain why clinical severity and outbreak size vary between locations and seasons." + citation(7, 8, 9),
    ], styles)
    add_subsection(story, "Environmental Factors", [
        "The immediate environmental requirement for most transmission is the presence of competent <i>Aedes</i> mosquitoes and human-mosquito contact. Mosquitoes breed in water-holding containers around homes, schools, construction sites, and commercial areas. High human density, unreliable water supply that encourages water storage, inadequate waste management, and weak vector-control coverage increase risk.",
        "Temperature and rainfall influence mosquito survival, biting frequency, larval habitats, and the extrinsic incubation period of the virus. Climate change can shift the geography and seasonality of vector suitability, but local infrastructure, housing, immunity, and public-health response determine whether ecological suitability becomes sustained transmission." + citation(1, 5, 6),
    ], styles)
    add_subsection(story, "Other Contributing Factors", [
        "Individual risk increases with exposure to daytime-biting mosquitoes, travel to areas with active transmission, absence of window screens or repellents, and limited ability to seek timely care. At the clinical level, prior infection with a heterologous serotype, pregnancy, young or advanced age, and chronic disease can warrant closer observation.",
        "Health-system factors are equally important. Delayed diagnosis, inability to monitor hematocrit and platelet trends, inadequate access to isotonic fluids, and late referral can turn a treatable critical-phase illness into shock or organ failure. Risk reduction therefore requires both household measures and reliable clinical pathways." + citation(3, 4, 10),
    ], styles)

    add_section(story, "4. Pathophysiology", styles)
    add_subsection(story, "Disease Mechanism", [
        "After an infected mosquito inoculates virus into the skin, DENV infects susceptible cells including dendritic cells and monocytes, then disseminates through lymphatic and blood compartments. Viral replication produces viremia and triggers innate and adaptive immune responses. Most infections resolve, but some patients develop an amplified inflammatory and vascular response during the critical phase.",
        "Severe dengue is characterized by increased endothelial permeability, which permits plasma to move into pleural, peritoneal, or other extravascular spaces. The resulting hemoconcentration and reduced effective circulating volume can cause compensated shock and then hypotensive shock. Severe bleeding and major organ involvement can occur independently or together with plasma leakage." + citation(4, 9, 12),
    ], styles)
    add_subsection(story, "Molecular and Cellular Changes", [
        "DENV non-structural protein 1 (NS1), complement activation, cytokine release, and altered endothelial glycocalyx function are implicated in endothelial dysfunction. Activated monocytes, T cells, B cells, complement pathways, and soluble mediators can intensify the inflammatory response. Thrombocytopenia arises through decreased production, peripheral destruction, consumption, and platelet activation; it is a useful monitoring marker but does not by itself predict bleeding severity.",
        "Antibody-dependent enhancement is a leading explanation for why some secondary infections are more severe. Pre-existing, cross-reactive antibodies may bind a new serotype without fully neutralizing it and facilitate infection of Fc receptor-bearing cells. This mechanism is biologically important but does not account for every severe case; severity remains multifactorial." + citation(9, 10, 11),
    ], styles)
    story.append(info_box("Pathophysiology in one line", "Severe dengue is primarily a problem of transient capillary leakage and intravascular volume loss, not simply low platelet count. Clinical fluid decisions should be guided by perfusion, urine output, hematocrit trends, and repeated examination.", styles))

    add_section(story, "5. Clinical Manifestations", styles)
    add_subsection(story, "Signs and Symptoms", [
        "After an incubation period of approximately 4-10 days, symptomatic dengue commonly causes abrupt fever, severe headache, retro-orbital pain, myalgia, arthralgia, nausea, vomiting, rash, and fatigue. Mild mucosal bleeding, leukopenia, and a positive tourniquet test may be present. Clinical features overlap with malaria, chikungunya, Zika, enteric fever, leptospirosis, influenza, and other febrile illnesses, so local epidemiology and travel history are essential.",
        "Warning signs include severe abdominal pain or tenderness, persistent vomiting, clinical fluid accumulation, mucosal bleeding, lethargy or restlessness, liver enlargement, and rising hematocrit with rapidly falling platelets. Severe dengue is defined by severe plasma leakage leading to shock or respiratory distress, severe bleeding, or severe organ involvement such as hepatitis, encephalopathy, myocarditis, or renal impairment." + citation(2, 3, 4),
    ], styles)
    add_subsection(story, "Disease Progression", [
        "The febrile phase usually lasts 2-7 days. The critical phase, if it occurs, often begins as the fever subsides and usually lasts 24-48 hours. This is the interval in which plasma leakage, shock, bleeding, and organ injury can evolve quickly. The recovery phase follows as vascular permeability normalizes and extravascular fluid is reabsorbed.",
        "A rising hematocrit with clinical deterioration suggests plasma leakage, whereas a falling hematocrit with instability may suggest bleeding or over-resuscitation. Serial trends are more useful than single values. Patients should be instructed to return immediately if warning signs emerge, even if the fever has improved." + citation(3, 4, 12),
    ], styles)
    story.append(data_table(
        ["Illness phase", "Typical features", "Clinical priority"],
        [
            ["Febrile", "Fever, headache, myalgia, rash, nausea; viremia is usually detectable early.", "Hydration, symptom relief, diagnostic testing, daily reassessment when indicated."],
            ["Critical", "Often near defervescence; plasma leakage, rising hematocrit, thrombocytopenia, warning signs, shock may occur.", "Frequent observations and carefully titrated isotonic fluids when needed."],
            ["Recovery", "Improved appetite and perfusion; reabsorption of extravascular fluid; fatigue may persist.", "Reduce IV fluids promptly when appropriate and watch for fluid overload."],
        ], [3.0 * cm, 7.1 * cm, 6.1 * cm], styles))

    add_section(story, "6. Diagnosis", styles)
    add_subsection(story, "Diagnostic Criteria", [
        "Diagnosis combines compatible symptoms, exposure history, physical examination, and laboratory evidence. A clinician should suspect dengue in a person with acute fever who lives in or has recently travelled to an area with dengue risk, especially if headache, retro-orbital pain, myalgia, arthralgia, rash, leukopenia, or warning signs are present. Management should begin on clinical grounds when suspicion is high; it should not wait for a test result.",
        "WHO classification separates dengue without warning signs, dengue with warning signs, and severe dengue. This clinical framework supports triage because patients with warning signs, severe disease, significant comorbidity, pregnancy, unreliable follow-up, or poor oral intake require a lower threshold for observation or admission." + citation(2, 3, 4),
    ], styles)
    add_subsection(story, "Laboratory Tests", [
        "During the first 0-7 days after symptom onset, NAAT such as RT-PCR plus IgM, or NS1 antigen plus IgM, is recommended where available. A positive NAAT or NS1 result supports confirmed acute infection. A negative NAAT or NS1 test does not exclude dengue, particularly later in the acute window. After day 7, IgM testing is the principal diagnostic test; paired serology may help establish recent infection.",
        "A complete blood count is central to clinical monitoring. Leukopenia, thrombocytopenia, and rising hematocrit may occur, but values must be interpreted with hydration status and clinical condition. Liver enzymes, renal function, electrolytes, coagulation studies, blood group and crossmatch, and lactate may be appropriate in patients with warning signs, bleeding, shock, or organ dysfunction. Serologic cross-reactivity with other flaviviruses may require expert interpretation or neutralization testing." + citation(2, 4),
    ], styles)
    add_subsection(story, "Imaging Techniques", [
        "Imaging is not required to diagnose uncomplicated dengue. Bedside ultrasound, chest radiography, or echocardiography may be useful when the clinician suspects plasma leakage, pleural effusion, ascites, pericardial effusion, pulmonary edema, cardiac dysfunction, or another diagnosis. Imaging findings support severity assessment but must be integrated with examination and hemodynamic data.",
    ], styles)
    add_subsection(story, "Genetic Testing", [
        "Routine host genetic testing has no role in dengue diagnosis or standard clinical management. Viral genotyping is used in surveillance, outbreak investigation, and research to track circulating serotypes and lineages. Research into host susceptibility is valuable, but no validated genetic test currently determines an individual's clinical course in routine practice." + citation(7, 8),
    ], styles)
    story.append(data_table(
        ["Timing after symptom onset", "Useful tests", "Key limitation"],
        [
            ["Days 0-7", "NAAT (for example RT-PCR) plus IgM, or NS1 antigen plus IgM.", "A negative NAAT or NS1 result does not rule out infection."],
            ["After day 7", "DENV IgM; consider paired serology when needed.", "IgM may cross-react with other flaviviruses and may persist for months."],
            ["Any phase", "CBC and targeted chemistry tests for severity monitoring.", "No single hematology value independently defines severe dengue."],
        ], [3.7 * cm, 7.3 * cm, 5.2 * cm], styles))

    add_section(story, "7. Treatment and Management", styles)
    add_subsection(story, "Pharmacological Management", [
        "There is no specific antiviral treatment routinely recommended for dengue. Paracetamol (acetaminophen) is used for fever and pain within usual safe dosing limits. Aspirin and non-steroidal anti-inflammatory drugs, including ibuprofen, should be avoided because they may increase bleeding risk. Routine corticosteroids and prophylactic platelet transfusions are not recommended.",
        "Blood products are reserved for clinically significant bleeding with hemodynamic compromise or evidence suggesting occult bleeding, not for an isolated low platelet count. Medication review is important because anticoagulants, antiplatelet agents, nephrotoxic drugs, and hepatotoxic medicines may affect risk or management decisions." + citation(1, 3, 4),
    ], styles)
    add_subsection(story, "Non-Pharmacological Management", [
        "Patients without warning signs who tolerate oral fluids, have reliable follow-up, normal urine output, and no important social or medical risk factor can often be managed as outpatients. Oral rehydration, rest, daily or clinically indicated review, and written return precautions are essential. Patients and families should be told that the period after fever resolution can be dangerous.",
        "Prevention during illness also matters. A viremic person can infect mosquitoes that bite them. Use of bed nets, screens, protective clothing, and repellent can reduce household transmission. Community measures include source reduction, covering water containers, solid-waste management, larval control, targeted adult mosquito control during outbreaks, and risk communication." + citation(1, 3),
    ], styles)
    add_subsection(story, "Supportive Care", [
        "Supportive care is the cornerstone of severe-dengue management. Patients with warning signs require close monitoring of vital signs, mental status, peripheral perfusion, urine output, intake and output, hematocrit, and other laboratory values. Isotonic crystalloid fluids are used when intravenous resuscitation is indicated, with repeated reassessment to give enough fluid for perfusion while avoiding overload.",
        "Admission and critical-care decisions depend on shock, respiratory distress, severe bleeding, altered consciousness, significant organ injury, pregnancy, comorbidity, age, and ability to return for follow-up. The best outcomes come from early identification, serial reassessment, meticulous fluid balance, and rapid access to a higher level of care." + citation(3, 4, 12),
    ], styles)
    story.append(info_box("Safety note", "Severe dengue is a medical emergency. This report is for academic use and does not replace local protocols, bedside assessment, or urgent medical care for warning signs.", styles))

    add_section(story, "8. Challenges and Future Perspectives", styles)
    add_subsection(story, "Challenges in Diagnosis and Treatment", [
        "Early dengue resembles many other febrile illnesses, and symptoms can be non-specific before warning signs develop. Laboratory capacity is uneven, rapid tests vary in performance, and serology can cross-react with other flaviviruses. In areas where dengue, chikungunya, Zika, malaria, leptospirosis, and enteric fever overlap, clinicians need practical algorithms and accessible confirmatory testing.",
        "Treatment remains supportive, so outcomes depend strongly on timely diagnosis and skilled fluid management. Outbreaks can overwhelm emergency departments and laboratories, while public-health programmes may struggle with insecticide resistance, fragmented urban services, household water storage, and inequitable access to care. Vaccine policies are evolving and must be matched to local epidemiology, product indication, individual risk, and national guidance." + citation(1, 2, 8),
    ], styles)
    add_subsection(story, "Future Research Directions", [
        "Priorities include safe antiviral therapies, improved point-of-care molecular and antigen tests, biomarkers that predict progression before shock occurs, and better understanding of endothelial injury. Prospective cohorts that include children, pregnant people, older adults, and communities with diverse prior exposure patterns are needed to improve risk stratification.",
        "Vector-control research is also essential. Integrated approaches may combine environmental management, targeted insecticide use, mosquito surveillance, <i>Wolbachia</i>-based strategies, community participation, and climate-informed early warning. Effective vaccines and delivery strategies could reduce disease burden when they are incorporated responsibly into broader surveillance and vector-control programmes." + citation(1, 8, 13),
    ], styles)

    add_section(story, "Conclusion", styles)
    story.append(p(
        "Dengue fever is not a rare disease; it is a rapidly changing global health challenge driven by mosquito ecology, urbanization, mobility, climate, viral diversity, and population immunity. Most patients recover with appropriate outpatient care, but a narrow critical window can lead to severe plasma leakage, shock, bleeding, or organ dysfunction. Accurate diagnosis, vigilant monitoring around defervescence, careful supportive management, and timely referral are central to preventing death. Sustainable control requires strong surveillance, diagnostic access, patient education, integrated vector management, and continued research into vaccines, therapeutics, and predictors of severe disease." + citation(1, 3, 4),
        styles["Body"],
    ))

    story.append(PageBreak())
    add_section(story, "References", styles)
    story.append(p("References are formatted in Vancouver style. Access dates are included for web guidance that is updated periodically.", styles["SmallNote"]))
    references = [
        "1. World Health Organization. Dengue [Internet]. Geneva: World Health Organization; 2025 Aug 21 [cited 2026 Jul 19]. Available from: https://www.who.int/news-room/fact-sheets/detail/dengue-and-severe-dengue",
        "2. Centers for Disease Control and Prevention. Clinical testing guidance for dengue [Internet]. Atlanta (GA): CDC; 2025 Aug 26 [cited 2026 Jul 19]. Available from: https://www.cdc.gov/dengue/hcp/diagnosis-testing/index.html",
        "3. Centers for Disease Control and Prevention. Clinical care of dengue [Internet]. Atlanta (GA): CDC; 2026 Apr 15 [cited 2026 Jul 19]. Available from: https://www.cdc.gov/dengue/hcp/clinical-care/index.html",
        "4. World Health Organization. Dengue: guidelines for diagnosis, treatment, prevention and control. New ed. Geneva: World Health Organization; 2009.",
        "5. Bhatt S, Gething PW, Brady OJ, Messina JP, Farlow AW, Moyes CL, et al. The global distribution and burden of dengue. Nature. 2013;496(7446):504-7. doi:10.1038/nature12060.",
        "6. Gubler DJ. Dengue and dengue hemorrhagic fever. Clin Microbiol Rev. 1998;11(3):480-96. doi:10.1128/CMR.11.3.480.",
        "7. Guzman MG, Harris E. Dengue. Lancet. 2015;385(9966):453-65. doi:10.1016/S0140-6736(14)60572-9.",
        "8. Wilder-Smith A, Ooi EE, Horstick O, Wills B. Dengue. Lancet. 2019;393(10169):350-63. doi:10.1016/S0140-6736(18)32560-1.",
        "9. Martina BEE, Koraka P, Osterhaus ADME. Dengue virus pathogenesis: an integrated view. Clin Microbiol Rev. 2009;22(4):564-81. doi:10.1128/CMR.00035-09.",
        "10. Halstead SB. Dengue. Lancet. 2007;370(9599):1644-52. doi:10.1016/S0140-6736(07)61687-0.",
        "11. Katzelnick LC, Gresh L, Halloran ME, Mercado JC, Kuan G, Gordon A, et al. Antibody-dependent enhancement of severe dengue disease in humans. Science. 2017;358(6365):929-32. doi:10.1126/science.aan6836.",
        "12. Simmons CP, Farrar JJ, Nguyen VVC, Wills B. Dengue. N Engl J Med. 2012;366(15):1423-32. doi:10.1056/NEJMra1110265.",
        "13. Stanaway JD, Shepard DS, Undurraga EA, Halasa YA, Coffeng LE, Brady OJ, et al. The global burden of dengue: an analysis from the Global Burden of Disease Study 2013. Lancet Infect Dis. 2016;16(6):712-23. doi:10.1016/S1473-3099(16)00026-8.",
        "14. Pan American Health Organization. Guidelines for clinical diagnosis and treatment of dengue, chikungunya, and Zika. Washington (DC): PAHO; 2021.",
    ]
    story.extend(p(reference, styles["Reference"]) for reference in references)
    return story


def main():
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    document = SimpleDocTemplate(
        str(OUTPUT_PATH), pagesize=A4,
        leftMargin=1.8 * cm, rightMargin=1.8 * cm,
        topMargin=2.05 * cm, bottomMargin=1.7 * cm,
        title="Dengue Fever: Project Report",
        author="Academic Project Submission",
        subject="Comprehensive clinical, epidemiological, and public health review of dengue fever",
    )
    document.build(make_story(build_styles()), onFirstPage=first_page, onLaterPages=later_pages)
    print(f"Created {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
