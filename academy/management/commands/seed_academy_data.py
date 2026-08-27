"""
Database seeder command for WIN PROFESSIONAL ACADEMY.
Populates official Academy profile, course categories, 5 Mathematics courses,
6 admission guidance streams, sample study materials, and results.
"""
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from academy.models import (
    AcademyProfile,
    CourseCategory,
    Course,
    CourseMaterial,
    AdmissionGuidanceStream,
    Result,
)


class Command(BaseCommand):
    help = "Seed initial production data for WIN PROFESSIONAL ACADEMY"

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Seeding WIN PROFESSIONAL ACADEMY database..."))

        # 1. Academy Profile & Branding
        profile, created = AcademyProfile.objects.get_or_create(id=1)
        profile.academy_name = "WIN PROFESSIONAL ACADEMY"
        profile.trust_name = "Win Educational Trust"
        profile.trust_reg_no = "379/2006"
        profile.tagline = "A Complete Guidelines for Higher Education & Job Service"
        profile.primary_phone = "63817 06581"
        profile.secondary_phone = "86681 8494"
        profile.email = "contact@winacademy.edu.in"
        profile.address = "Tamil Nadu, India"
        profile.whatsapp_number = "6381706581"
        profile.mission = (
            "To empower students across Tamil Nadu and India with expert guidance for higher education "
            "admissions and rigorous, results-oriented competitive coaching in Mathematics and professional careers."
        )
        profile.vision = (
            "To stand as the most trusted educational sanctuary where every student achieves their academic "
            "ambition in top medical, engineering, agricultural, law, and arts institutions, and excels in prestigious competitive exams."
        )
        profile.higher_education_guidance = (
            "Expert personalized counseling, college selection, eligibility mapping, and admission assistance "
            "for Medical, Paramedical, Engineering, Agriculture, Law, and Arts & Science colleges across Tamil Nadu, "
            "all-India centralized admissions, and accredited universities abroad."
        )
        profile.job_services_guidance = (
            "Targeted coaching, structured question bank mastery, conceptual problem-solving, and career mentorship "
            "for teaching recruitment (UG/PG TRB), government eligibility (CSIR-NET JRF, GATE), and professional job opportunities."
        )
        profile.save()
        self.stdout.write(self.style.SUCCESS("[OK] Academy profile & branding seeded."))

        # 2. Course Categories
        math_cat, _ = CourseCategory.objects.get_or_create(
            slug="mathematics-coaching",
            defaults={
                'name': "Mathematics Coaching & Competitive Exams",
                'description': "Specialized, concept-driven coaching for university mathematics and national/state level competitive examinations.",
                'display_order': 1,
                'is_active': True,
            }
        )

        guidance_cat, _ = CourseCategory.objects.get_or_create(
            slug="higher-education-guidance",
            defaults={
                'name': "Higher Education & Admission Guidance",
                'description': "Comprehensive admission guidance and career counseling across professional streams.",
                'display_order': 2,
                'is_active': True,
            }
        )
        self.stdout.write(self.style.SUCCESS("[OK] Course categories created."))

        # 3. Five Mathematics Courses
        courses_data = [
            {
                'title': "Engineering Mathematics",
                'slug': "engineering-mathematics",
                'category': math_cat,
                'target_audience': "For College & University Students",
                'short_description': "Comprehensive coaching in Linear Algebra, Calculus, Differential Equations, Transforms, and Numerical Methods for Engineering undergraduates.",
                'full_description': (
                    "Engineering Mathematics is the foundational pillar for all engineering disciplines. "
                    "Our specialized course covers all university syllabus requirements (Anna University, Autonomous & Deemed Universities). "
                    "We emphasize clear conceptual derivations, step-by-step problem-solving techniques, model exam papers, and university question bank mastery to ensure university distinction."
                ),
                'syllabus': (
                    "Matrices & Linear Algebra (Eigenvalues, Eigenvectors, Cayley-Hamilton)\n"
                    "Differential & Integral Calculus (Curvature, Evolutes, Multiple Integrals)\n"
                    "Ordinary & Partial Differential Equations\n"
                    "Vector Calculus & Complex Analysis (Analytic Functions, Contour Integration)\n"
                    "Laplace Transforms & Fourier Analysis (Z-Transforms, Fourier Series)\n"
                    "Probability, Statistics & Numerical Methods"
                ),
                'duration': "Semester-wise / Fast-track Crash Courses",
                'eligibility': "B.E / B.Tech / Diploma Students across all branches",
                'batch_mode': "Classroom & Interactive Live Sessions",
                'display_order': 1,
                'is_featured': True,
            },
            {
                'title': "UG / PG TRB Mathematics",
                'slug': "ug-pg-trb-mathematics",
                'category': math_cat,
                'target_audience': "Competitive Examination Coaching",
                'short_description': "Rigorous preparation for Teachers Recruitment Board (TRB) examinations for Assistant Professors, PG Assistants, and Graduate Teachers in Tamil Nadu.",
                'full_description': (
                    "Comprehensive syllabus mastery and high-yield question solving tailored strictly to the Tamil Nadu TRB examination pattern. "
                    "Includes unit-wise study notes, daily formula drills, shortcut techniques, previous years' solved question banks, and simulated state-level mock tests."
                ),
                'syllabus': (
                    "Unit 1: Real Analysis & Metric Spaces\n"
                    "Unit 2: Complex Analysis & Residue Calculus\n"
                    "Unit 3: Modern Algebra (Groups, Rings, Fields, Vector Spaces)\n"
                    "Unit 4: Operations Research & Linear Programming\n"
                    "Unit 5: Differential Equations & Classical Mechanics\n"
                    "Unit 6: Statistics, Probability Distributions & Sampling Theory\n"
                    "Unit 7: Numerical Methods & Mathematical Physics\n"
                    "Unit 8: Differential Geometry & Topology"
                ),
                'duration': "6 Months Comprehensive / Weekend Batches",
                'eligibility': "B.Sc / M.Sc Mathematics + B.Ed Aspirants",
                'batch_mode': "Intensive Classroom & Online Mentorship",
                'display_order': 2,
                'is_featured': True,
            },
            {
                'title': "CSIR-NET Mathematical Sciences",
                'slug': "csir-net-mathematical-sciences",
                'category': math_cat,
                'target_audience': "Junior Research Fellowship (JRF) & Lectureship / Assistant Professorship",
                'short_description': "Comprehensive preparation for CSIR-UGC NET Mathematical Sciences with rigorous conceptual depth and advanced problem-solving.",
                'full_description': (
                    "Designed for post-graduate students aiming for JRF and Assistant Professorship. "
                    "Our structured methodology breaks down high-weightage topics in Pure & Applied Mathematics, with in-depth focus on Parts A, B, and C multi-correct analysis, previous 15 years' paper solutions, and weekly assessment tests."
                ),
                'syllabus': (
                    "Unit 1: Linear Algebra & Real Analysis (Point Set Topology, Riemann Integration, Uniform Convergence)\n"
                    "Unit 2: Complex Analysis, Abstract Algebra (Sylow Theorems, Galois Theory) & Number Theory\n"
                    "Unit 3: Ordinary & Partial Differential Equations, Calculus of Variations, Integral Equations & Classical Mechanics\n"
                    "Unit 4: Probability, Statistics, Markov Chains & Operational Research\n"
                    "General Aptitude & Reasoning (Part A Mastery)"
                ),
                'duration': "6 Months / 1 Year Comprehensive Batch",
                'eligibility': "M.Sc Mathematics / Final Year Students",
                'batch_mode': "Classroom & Hybrid Online Batches",
                'display_order': 3,
                'is_featured': True,
            },
            {
                'title': "GATE Mathematics",
                'slug': "gate-mathematics",
                'category': math_cat,
                'target_audience': "Focused preparation for GATE (MA Paper)",
                'short_description': "Targeted GATE Mathematics coaching for admissions into M.Tech/Ph.D at IITs/IISc and executive PSU recruitment.",
                'full_description': (
                    "Focused, highly analytical coaching targeting high GATE scores (MA paper). "
                    "Emphasizes accuracy, speed, Numerical Answer Type (NAT) calculation strategies, standard proofs, and full-length online test series matching the official GATE interface."
                ),
                'syllabus': (
                    "Calculus & Vector Calculus\n"
                    "Linear Algebra & Matrix Theory\n"
                    "Real Analysis & Metric Spaces\n"
                    "Complex Analysis\n"
                    "Ordinary & Partial Differential Equations\n"
                    "Functional Analysis & Topology\n"
                    "Numerical Analysis & Linear Programming"
                ),
                'duration': "6 Months Intensive Coaching",
                'eligibility': "B.Sc/M.Sc Maths, B.E/B.Tech with Maths background",
                'batch_mode': "Classroom & Live Weekend Sessions",
                'display_order': 4,
                'is_featured': True,
            },
            {
                'title': "JAM Mathematics",
                'slug': "jam-mathematics",
                'category': math_cat,
                'target_audience': "Complete preparation for IIT-JAM Mathematics",
                'short_description': "Complete preparation for IIT-JAM Mathematics for admission to M.Sc programs at IITs, IISc, and NITs.",
                'full_description': (
                    "Specialized program designed for undergraduate mathematics students seeking entrance into premier national institutes (IITs, IISc, IISERs, NITs). "
                    "Features foundational concept building, speed enhancement drills, topic-wise practice sheets, and comprehensive mock exams."
                ),
                'syllabus': (
                    "Sequences and Series of Real Numbers\n"
                    "Functions of One Real Variable (Continuity, Differentiability, Taylor's Theorem)\n"
                    "Multivariable Calculus (Double & Triple Integrals, Line Integrals, Green's/Stokes' Theorems)\n"
                    "Differential Equations (First & Second Order Linear Equations)\n"
                    "Vector Calculus\n"
                    "Group Theory (Cyclic Groups, Permutation Groups, Homomorphisms)\n"
                    "Linear Algebra (Vector Spaces, Linear Transformations, Rank-Nullity Theorem)"
                ),
                'duration': "1 Year Foundation / 6 Months Crash Batch",
                'eligibility': "B.Sc Mathematics / B.A Mathematics (1st, 2nd, 3rd year)",
                'batch_mode': "Classroom & Digital Interactive Sessions",
                'display_order': 5,
                'is_featured': True,
            },
        ]

        for item in courses_data:
            course, _ = Course.objects.update_or_create(
                slug=item['slug'],
                defaults=item
            )
            # Create a sample study material note for each course
            CourseMaterial.objects.get_or_create(
                course=course,
                title=f"{course.title} - Quick Reference Formula Sheet & Notes",
                defaults={
                    'description': f"Official syllabus highlights, high-yield formula compendium, and overview notes for {course.title}.",
                    'material_type': 'NOTE',
                    'is_public': True,
                    'display_order': 1,
                }
            )

        self.stdout.write(self.style.SUCCESS("[OK] 5 Mathematics courses and study material references seeded."))

        # 4. Admission Guidance Streams
        streams_data = [
            {
                'name': "Medical Guidance",
                'slug': "medical",
                'scope': "ALL",
                'icon_name': "fa-user-md",
                'short_description': "Expert counseling and admission pathways for MBBS, BDS, and AYUSH in top government & private medical colleges across Tamil Nadu, all-India seats, and international medical universities.",
                'key_specializations': "MBBS, BDS, BAMS, BHMS, BSMS",
                'display_order': 1,
            },
            {
                'name': "Paramedical Guidance",
                'slug': "paramedical",
                'scope': "ALL",
                'icon_name': "fa-heartbeat",
                'short_description': "Complete admissions support for critical allied health science programs with strong hospital training and global healthcare career opportunities.",
                'key_specializations': "B.Sc Nursing, B.Pharm, BPT Physiotherapy, B.Sc Radiology, Medical Lab Tech",
                'display_order': 2,
            },
            {
                'name': "Engineering Admissions",
                'slug': "engineering",
                'scope': "ALL",
                'icon_name': "fa-cogs",
                'short_description': "Strategic guidance for TNEA single-window counseling, premier autonomous institutions, top deemed universities, and national institutes across India.",
                'key_specializations': "Computer Science, AI & Data Science, ECE, Mechanical, Civil, Robotics, Biotechnology",
                'display_order': 3,
            },
            {
                'name': "Agriculture & Horticulture",
                'slug': "agriculture",
                'scope': "ALL",
                'icon_name': "fa-leaf",
                'short_description': "Guidance for prestigious TNAU constituent & affiliated colleges, ICAR accredited agricultural universities across India with high placement and civil service prospects.",
                'key_specializations': "B.Sc (Hons) Agriculture, Horticulture, Agricultural Engineering, Food Tech",
                'display_order': 4,
            },
            {
                'name': "Law & Legal Studies",
                'slug': "law",
                'scope': "ALL",
                'icon_name': "fa-balance-scale",
                'short_description': "Guidance for 5-Year Integrated Honors Law & 3-Year LLB programs under TNDALU (School of Excellence in Law) and leading National Law Universities (NLUs).",
                'key_specializations': "BA LLB (Hons), BBA LLB (Hons), B.Com LLB, 3-Year LLB, LLM",
                'display_order': 5,
            },
            {
                'name': "Arts & Science Programs",
                'slug': "arts-and-science",
                'scope': "ALL",
                'icon_name': "fa-university",
                'short_description': "Admission guidance for premier autonomous Arts & Science institutions in Tamil Nadu and central universities for pure sciences, commerce, and computer applications.",
                'key_specializations': "B.Sc Mathematics, B.Sc Computer Science, B.Com (Gen/PA/CS), BCA, BBA, M.Sc, MCA",
                'display_order': 6,
            },
        ]

        for s_data in streams_data:
            AdmissionGuidanceStream.objects.update_or_create(
                slug=s_data['slug'],
                defaults=s_data
            )
        self.stdout.write(self.style.SUCCESS("[OK] 6 Admission guidance streams seeded."))

        # 5. Sample Student Results & Achievements
        results_data = [
            {
                'student_name': "K. Priya",
                'examination': "CSIR-NET Mathematical Sciences",
                'year': "2025-2026",
                'rank': "AIR 24 (JRF)",
                'score': "118.5 Marks",
                'description': "Qualified for CSIR-NET JRF in first attempt through Win Professional Academy's systematic conceptual coaching and rigorous Part C problem sessions.",
                'is_featured': True,
                'display_order': 1,
            },
            {
                'student_name': "R. Vignesh",
                'examination': "GATE Mathematics",
                'year': "2025-2026",
                'rank': "AIR 58",
                'score': "GATE Score: 782",
                'description': "Secured M.Tech/Ph.D admission in IIT Madras with high percentile. The formula sheets and online test series were invaluable.",
                'is_featured': True,
                'display_order': 2,
            },
            {
                'student_name': "S. Kavitha",
                'examination': "PG TRB Mathematics",
                'year': "2024-2025",
                'rank': "State Rank 4",
                'score': "124 / 150",
                'description': "Selected as PG Assistant in Government Higher Secondary School. The unit-wise test series and shortcut methods provided complete confidence.",
                'is_featured': True,
                'display_order': 3,
            },
            {
                'student_name': "M. Dinesh Kumar",
                'examination': "IIT-JAM Mathematics",
                'year': "2025-2026",
                'rank': "AIR 89",
                'score': "Marks: 64.33",
                'description': "Joined IIT Bombay for M.Sc Mathematics. Highly thankful to the faculty for crystal-clear Real & Linear Algebra concepts.",
                'is_featured': True,
                'display_order': 4,
            },
            {
                'student_name': "A. Sharmila",
                'examination': "UG TRB Graduate Teacher",
                'year': "2024-2025",
                'rank': "District Rank 1",
                'score': "116 / 150",
                'description': "Achieved district first rank in Mathematics. Win Academy's continuous motivation and comprehensive notes were the driving force.",
                'is_featured': True,
                'display_order': 5,
            },
            {
                'student_name': "V. Manikandan",
                'examination': "Engineering Mathematics Distinction",
                'year': "2025-2026",
                'rank': "University Grade 'O'",
                'score': "98 / 100",
                'description': "Secured Grade 'O' (Outstanding) in Engineering Mathematics I & II across Anna University semesters.",
                'is_featured': True,
                'display_order': 6,
            },
        ]

        for r_data in results_data:
            Result.objects.update_or_create(
                student_name=r_data['student_name'],
                examination=r_data['examination'],
                defaults=r_data
            )
        self.stdout.write(self.style.SUCCESS("[OK] Student results & achievements seeded."))
        self.stdout.write(self.style.SUCCESS("[SUCCESS] WIN PROFESSIONAL ACADEMY database seeding completed successfully!"))
