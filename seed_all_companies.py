import os
import django
from datetime import timedelta
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from accounts.models import User, Company
from jobs.models import Job

COMPANIES_DATA = [
    # ==========================================
    # 1. PRODUCT BASED COMPANIES
    # ==========================================
    {
        'username': 'recruiter_google',
        'email': 'careers@google.com',
        'company_name': 'Google',
        'company_type': Company.CompanyType.PRODUCT,
        'website': 'https://careers.google.com',
        'location': 'Bangalore & Hyderabad, India',
        'industry': 'Search, Cloud & Artificial Intelligence',
        'description': (
            'Google is a global technology leader focused on improving the ways people connect with information. '
            'Our innovations in web search, cloud computing, machine learning, Android, and software infrastructure '
            'power billions of users every day across the globe.'
        ),
        'jobs': [
            {
                'title': 'Software Engineer - Backend & Distributed Systems',
                'job_type': Job.JobType.FULL_TIME,
                'location': 'Bangalore, India (Hybrid)',
                'salary_min': 2800000,
                'salary_max': 4500000,
                'experience': 2,
                'skills': 'Python, Go, C++, Distributed Systems, Cloud Architecture, Algorithms',
                'description': (
                    'Join Google Cloud engineering team building hyperscale infrastructure. You will design, develop, '
                    'test, deploy, maintain, and enhance large-scale distributed software solutions.'
                ),
                'responsibilities': (
                    '- Write scalable, robust, and unit-tested code in Python or Go.\n'
                    '- Build APIs and cloud microservices serving millions of queries per second.\n'
                    '- Collaborate with product management and site reliability teams.'
                ),
            },
            {
                'title': 'Junior Software Developer (Python / Cloud)',
                'job_type': Job.JobType.FULL_TIME,
                'location': 'Hyderabad, India',
                'salary_min': 1800000,
                'salary_max': 2600000,
                'experience': 0,
                'skills': 'Python, Django, Data Structures, Algorithms, SQL, Git',
                'description': (
                    'Kickstart your career at Google working with engineering mentors. Build internal tools, automated pipelines, '
                    'and microservices supporting Google developer ecosystems.'
                ),
                'responsibilities': (
                    '- Implement backend services and REST APIs with Python.\n'
                    '- Write unit tests and participate in design and code reviews.\n'
                    '- Diagnose performance bottlenecks and improve database queries.'
                ),
            },
        ],
    },
    {
        'username': 'recruiter_microsoft',
        'email': 'careers@microsoft.com',
        'company_name': 'Microsoft',
        'company_type': Company.CompanyType.PRODUCT,
        'website': 'https://careers.microsoft.com',
        'location': 'Hyderabad & Bangalore, India',
        'industry': 'Cloud, Operating Systems & Productivity SaaS',
        'description': (
            'Microsoft enables digital transformation for the era of an intelligent cloud and an intelligent edge. '
            'Its mission is to empower every person and every organization on the planet to achieve more through Azure, '
            'Microsoft 365, Teams, and Copilot AI technologies.'
        ),
        'jobs': [
            {
                'title': 'Full Stack Cloud Engineer (React & Python)',
                'job_type': Job.JobType.FULL_TIME,
                'location': 'Hyderabad, India',
                'salary_min': 2400000,
                'salary_max': 3800000,
                'experience': 3,
                'skills': 'Python, React, TypeScript, Azure, REST API, Docker',
                'description': (
                    'Build next-generation developer tooling for Microsoft Azure cloud management portals. '
                    'You will bridge sleek React web frontends with resilient Python and microservice backends.'
                ),
                'responsibilities': (
                    '- Develop rich, responsive web applications in React and TypeScript.\n'
                    '- Build scalable RESTful APIs on Azure Cloud services.\n'
                    '- Ensure highest standards of accessibility, performance, and security.'
                ),
            },
            {
                'title': 'Cloud Security & Infrastructure Intern',
                'job_type': Job.JobType.INTERNSHIP,
                'location': 'Bangalore, India (Hybrid)',
                'salary_min': 600000,
                'salary_max': 900000,
                'experience': 0,
                'skills': 'Python, Linux, Networking, Cloud Security, Git',
                'description': (
                    '6-month engineering internship with Microsoft Azure Security team. Learn cloud network isolation, '
                    'automated vulnerability scanning, and CI/CD pipelines.'
                ),
                'responsibilities': (
                    '- Write automation scripts in Python for cloud configuration auditing.\n'
                    '- Assist in investigating security telemetries and threat logs.'
                ),
            },
        ],
    },
    {
        'username': 'recruiter_amazon',
        'email': 'recruiting@amazon.jobs',
        'company_name': 'Amazon',
        'company_type': Company.CompanyType.PRODUCT,
        'website': 'https://amazon.jobs',
        'location': 'Bangalore & Hyderabad, India',
        'industry': 'E-Commerce, Cloud (AWS) & Logistics',
        'description': (
            'Amazon is guided by four principles: customer obsession, passion for invention, commitment to operational excellence, '
            'and long-term thinking. Amazon Web Services (AWS) is the world’s most comprehensive and broadly adopted cloud.'
        ),
        'jobs': [
            {
                'title': 'Software Development Engineer I (SDE 1)',
                'job_type': Job.JobType.FULL_TIME,
                'location': 'Bangalore, India',
                'salary_min': 1800000,
                'salary_max': 2800000,
                'experience': 1,
                'skills': 'Java, Python, AWS, Data Structures, OOP, SQL',
                'description': (
                    'Join the Amazon Consumer Tech team developing high-volume fulfillment, catalog search, and payment services. '
                    'Solve challenging latency and scale challenges on AWS.'
                ),
                'responsibilities': (
                    '- Design and code modular microservices with high test coverage.\n'
                    '- Work with DynamoDB, SQS, SNS, and ECS containers.\n'
                    '- Optimize operational metrics and automated alerting.'
                ),
            },
            {
                'title': 'DevOps & Cloud Systems Engineer',
                'job_type': Job.JobType.FULL_TIME,
                'location': 'Hyderabad, India (or Remote)',
                'salary_min': 2200000,
                'salary_max': 3500000,
                'experience': 3,
                'skills': 'AWS, Terraform, Docker, Kubernetes, Python, CI/CD, Linux',
                'description': (
                    'Manage massive automated deployments, infrastructure-as-code, and continuous delivery pipelines across multi-region AWS environments.'
                ),
                'responsibilities': (
                    '- Provision infrastructure using Terraform and CloudFormation.\n'
                    '- Maintain Kubernetes clusters and container workloads.\n'
                    '- Automate build pipelines and monitor platform health.'
                ),
            },
        ],
    },
    {
        'username': 'recruiter_adobe',
        'email': 'talent@adobe.com',
        'company_name': 'Adobe',
        'company_type': Company.CompanyType.PRODUCT,
        'website': 'https://careers.adobe.com',
        'location': 'Noida & Bangalore, India',
        'industry': 'Digital Media, Creative SaaS & Document Cloud',
        'description': (
            'Adobe is changing the world through digital experiences. From Creative Cloud (Photoshop, Illustrator) '
            'to Adobe Experience Cloud and Acrobat, Adobe fuels creativity and paperless productivity worldwide.'
        ),
        'jobs': [
            {
                'title': 'Frontend Engineer (React, WebGL, TypeScript)',
                'job_type': Job.JobType.FULL_TIME,
                'location': 'Noida, India (Hybrid)',
                'salary_min': 2000000,
                'salary_max': 3200000,
                'experience': 2,
                'skills': 'JavaScript, TypeScript, React, HTML5, CSS3, WebGL, Redux',
                'description': (
                    'Build browser-based creative canvases and collaborative design tools within Adobe Creative Cloud Web applications.'
                ),
                'responsibilities': (
                    '- Build high-performance UI components with React and modern CSS.\n'
                    '- Implement 60fps canvas rendering and real-time collaboration features.\n'
                    '- Write unit tests and maintain cross-browser compatibility.'
                ),
            },
        ],
    },
    {
        'username': 'recruiter_atlassian',
        'email': 'careers@atlassian.com',
        'company_name': 'Atlassian',
        'company_type': Company.CompanyType.PRODUCT,
        'website': 'https://www.atlassian.com/company/careers',
        'location': 'Bangalore, India (Remote-First)',
        'industry': 'Enterprise Collaboration & Developer Tools',
        'description': (
            'Atlassian produces tools like Jira, Confluence, Bitbucket, and Trello that power teamwork across millions '
            'of software development, IT operations, and product teams around the globe.'
        ),
        'jobs': [
            {
                'title': 'Backend Engineer - Platform & APIs',
                'job_type': Job.JobType.REMOTE,
                'location': 'Remote (India)',
                'salary_min': 2600000,
                'salary_max': 4000000,
                'experience': 3,
                'skills': 'Python, Java, Spring Boot, REST API, GraphQL, PostgreSQL, Docker',
                'description': (
                    'Work on the Atlassian Cloud platform powering Jira workflows. Design public REST and GraphQL APIs used by thousands of enterprise integration partners.'
                ),
                'responsibilities': (
                    '- Architect reliable and idempotent distributed APIs.\n'
                    '- Optimize query latencies on large PostgreSQL databases.\n'
                    '- Collaborate across global remote engineering squads.'
                ),
            },
        ],
    },
    {
        'username': 'recruiter_uber',
        'email': 'careers@uber.com',
        'company_name': 'Uber',
        'company_type': Company.CompanyType.PRODUCT,
        'website': 'https://www.uber.com/us/en/careers/',
        'location': 'Bangalore & Hyderabad, India',
        'industry': 'Mobility, Logistics & High-Throughput Distributed Systems',
        'description': (
            'Uber reimagines the way the world moves for the better. The technology team in India builds fundamental systems '
            'for rider safety, maps, payments, financial tech, and marketplace matching.'
        ),
        'jobs': [
            {
                'title': 'Systems Engineer (Go / Python / Kafka)',
                'job_type': Job.JobType.FULL_TIME,
                'location': 'Bangalore, India',
                'salary_min': 2800000,
                'salary_max': 4600000,
                'experience': 4,
                'skills': 'Go, Python, Kafka, Redis, Distributed Systems, Microservices, MySQL',
                'description': (
                    'Solve real-time dispatch and trip routing problems processing millions of concurrent geo-location events every second.'
                ),
                'responsibilities': (
                    '- Build ultra-low latency event streaming pipelines using Kafka.\n'
                    '- Develop fault-tolerant services in Go and Python.\n'
                    '- Participate in on-call operational reviews and performance tuning.'
                ),
            },
        ],
    },

    # ==========================================
    # 2. SERVICE BASED COMPANIES
    # ==========================================
    {
        'username': 'recruiter_tcs',
        'email': 'careers@tcs.com',
        'company_name': 'Tata Consultancy Services (TCS)',
        'company_type': Company.CompanyType.SERVICE,
        'website': 'https://www.tcs.com/careers',
        'location': 'Mumbai, Chennai, Hyderabad & Bangalore, India',
        'industry': 'IT Services, Business Consulting & Cloud Modernization',
        'description': (
            'Tata Consultancy Services (TCS) is an IT services, consulting, and business solutions organization '
            'that has been partnering with many of the world’s largest businesses in their transformation journeys for over 50 years.'
        ),
        'jobs': [
            {
                'title': 'Python / Django Application Developer',
                'job_type': Job.JobType.FULL_TIME,
                'location': 'Hyderabad, India',
                'salary_min': 650000,
                'salary_max': 1200000,
                'experience': 2,
                'skills': 'Python, Django, PostgreSQL, REST API, HTML5, Bootstrap, Git',
                'description': (
                    'Develop and modernize enterprise web applications for international banking and insurance clients. '
                    'Work in an agile environment with clear career progression.'
                ),
                'responsibilities': (
                    '- Develop full-stack modules using Django and relational databases.\n'
                    '- Build REST APIs for third-party client integrations.\n'
                    '- Write automated unit tests and participate in sprint planning.'
                ),
            },
            {
                'title': 'Graduate Trainee - Software Engineering',
                'job_type': Job.JobType.FULL_TIME,
                'location': 'Chennai, India',
                'salary_min': 400000,
                'salary_max': 550000,
                'experience': 0,
                'skills': 'Python, Java, SQL, OOP, Communication Skills, Problem Solving',
                'description': (
                    'Campus and fresher intake program. Comprehensive training in cloud development, enterprise databases, '
                    'and agile software delivery before project allocation.'
                ),
                'responsibilities': (
                    '- Complete technical certification modules during initial training.\n'
                    '- Assist senior team leads in module development and defect remediation.'
                ),
            },
        ],
    },
    {
        'username': 'recruiter_infosys',
        'email': 'careers@infosys.com',
        'company_name': 'Infosys',
        'company_type': Company.CompanyType.SERVICE,
        'website': 'https://www.infosys.com/careers/',
        'location': 'Bangalore, Pune, Hyderabad, India',
        'industry': 'Digital Services, Enterprise IT Consulting & AI Transformation',
        'description': (
            'Infosys is a global leader in next-generation digital services and consulting. We enable clients in more than '
            '56 countries to navigate their digital transformation powered by cloud and AI.'
        ),
        'jobs': [
            {
                'title': 'Senior Systems Engineer (Full Stack Python / React)',
                'job_type': Job.JobType.FULL_TIME,
                'location': 'Bangalore, India (Hybrid)',
                'salary_min': 800000,
                'salary_max': 1500000,
                'experience': 3,
                'skills': 'Python, Django, React, JavaScript, MySQL, Docker, CI/CD',
                'description': (
                    'Lead full stack web development for global retail and telecom transformation projects. '
                    'Manage sprint deliverables, code quality, and client communications.'
                ),
                'responsibilities': (
                    '- Design and implement backend REST endpoints in Django.\n'
                    '- Integrate modern React user interfaces with secure backend auth.\n'
                    '- Mentor junior developers on best coding practices.'
                ),
            },
            {
                'title': 'Associate Consultant - Data Engineering',
                'job_type': Job.JobType.FULL_TIME,
                'location': 'Pune, India',
                'salary_min': 900000,
                'salary_max': 1600000,
                'experience': 2,
                'skills': 'Python, SQL, ETL, Apache Spark, AWS, Snowflake',
                'description': (
                    'Design automated data pipelines, ETL workflows, and reporting dashboards for enterprise analytics customers.'
                ),
                'responsibilities': (
                    '- Extract, transform, and load data from heterogeneous enterprise databases.\n'
                    '- Optimize complex SQL queries and data warehouse schemas.'
                ),
            },
        ],
    },
    {
        'username': 'recruiter_wipro',
        'email': 'careers@wipro.com',
        'company_name': 'Wipro',
        'company_type': Company.CompanyType.SERVICE,
        'website': 'https://careers.wipro.com',
        'location': 'Bangalore, Hyderabad, Noida, India',
        'industry': 'IT Consulting, Cognitive Computing & Digital Solutions',
        'description': (
            'Wipro Limited is a leading technology services and consulting company focused on building innovative solutions '
            'that address clients’ most complex digital transformation needs.'
        ),
        'jobs': [
            {
                'title': 'Web Developer (Python, Django, JavaScript)',
                'job_type': Job.JobType.FULL_TIME,
                'location': 'Hyderabad, India',
                'salary_min': 600000,
                'salary_max': 1100000,
                'experience': 2,
                'skills': 'Python, Django, JavaScript, CSS3, HTML5, PostgreSQL',
                'description': (
                    'Develop responsive web portals, workflow engines, and reporting modules for global financial services clients.'
                ),
                'responsibilities': (
                    '- Develop backend models, views, and forms in Django.\n'
                    '- Ensure cross-browser responsiveness using Bootstrap and JavaScript.\n'
                    '- Conduct code reviews and unit test verifications.'
                ),
            },
        ],
    },
    {
        'username': 'recruiter_accenture',
        'email': 'careers@accenture.com',
        'company_name': 'Accenture',
        'company_type': Company.CompanyType.SERVICE,
        'website': 'https://www.accenture.com/careers',
        'location': 'Bangalore, Mumbai, Gurgaon, India',
        'industry': 'Management Consulting, Cloud & Technology Transformation',
        'description': (
            'Accenture is a leading global professional services company providing a broad range of services in strategy and consulting, '
            'technology and operations, with digital capabilities across all of these services.'
        ),
        'jobs': [
            {
                'title': 'Software Engineering Senior Analyst',
                'job_type': Job.JobType.FULL_TIME,
                'location': 'Bangalore, India (Hybrid)',
                'salary_min': 1000000,
                'salary_max': 1800000,
                'experience': 3,
                'skills': 'Python, Django, React, Cloud, Microservices, Agile, SQL',
                'description': (
                    'Collaborate directly with international Fortune 500 clients to architect robust, scalable digital platforms.'
                ),
                'responsibilities': (
                    '- Deliver end-to-end software modules from technical specifications.\n'
                    '- Coordinate with global business analysts and QA specialists.\n'
                    '- Champion automated testing and CI/CD best practices.'
                ),
            },
        ],
    },
    {
        'username': 'recruiter_cognizant',
        'email': 'careers@cognizant.com',
        'company_name': 'Cognizant',
        'company_type': Company.CompanyType.SERVICE,
        'website': 'https://careers.cognizant.com',
        'location': 'Chennai, Bangalore, Hyderabad, India',
        'industry': 'Digital Engineering, Enterprise Applications & Cloud Solutions',
        'description': (
            'Cognizant engineers modern businesses. We help our clients modernize technology, reimagine processes and '
            'transform experiences so they can stay ahead in a fast-changing world.'
        ),
        'jobs': [
            {
                'title': 'Associate Software Engineer (Python / API)',
                'job_type': Job.JobType.FULL_TIME,
                'location': 'Chennai, India',
                'salary_min': 550000,
                'salary_max': 950000,
                'experience': 1,
                'skills': 'Python, Flask, Django, SQL, REST API, Git',
                'description': (
                    'Develop API gateways and backend data pipelines for healthcare and life sciences client applications.'
                ),
                'responsibilities': (
                    '- Build well-documented RESTful web services in Python.\n'
                    '- Write automated test suites and ensure database query efficiency.'
                ),
            },
        ],
    },
    {
        'username': 'recruiter_techmahindra',
        'email': 'careers@techmahindra.com',
        'company_name': 'Tech Mahindra',
        'company_type': Company.CompanyType.SERVICE,
        'website': 'https://careers.techmahindra.com',
        'location': 'Pune, Hyderabad, Bangalore, India',
        'industry': 'Telecom, 5G, Enterprise IT & Digital Solutions',
        'description': (
            'Tech Mahindra represents the connected world, offering innovative and customer-centric information technology '
            'experiences across telecom, automotive, and financial services.'
        ),
        'jobs': [
            {
                'title': 'Cloud Integration Developer',
                'job_type': Job.JobType.FULL_TIME,
                'location': 'Pune, India',
                'salary_min': 600000,
                'salary_max': 1150000,
                'experience': 2,
                'skills': 'Python, Linux, Shell Scripting, Docker, REST API, MySQL',
                'description': (
                    'Implement integration middleware connecting telecom network hardware with cloud billing and orchestration platforms.'
                ),
                'responsibilities': (
                    '- Develop automation and integration scripts in Python and Bash.\n'
                    '- Configure monitoring agents and audit system logs.'
                ),
            },
        ],
    },

    # ==========================================
    # 3. HIGH-GROWTH STARTUPS
    # ==========================================
    {
        'username': 'recruiter_zepto',
        'email': 'careers@zeptonow.com',
        'company_name': 'Zepto',
        'company_type': Company.CompanyType.STARTUP,
        'website': 'https://www.zeptonow.com/careers',
        'location': 'Mumbai & Bangalore, India',
        'industry': 'Quick Commerce, Hyper-Local Logistics & Retail Tech',
        'description': (
            'Zepto is India’s fastest-growing quick-commerce unicorn delivering groceries and essentials in 10 minutes. '
            'Our engineering team builds high-concurrency dispatch engines, dark store robotics, and real-time inventory systems.'
        ),
        'jobs': [
            {
                'title': 'Backend Engineer - Dispatch & Dark Store Ops',
                'job_type': Job.JobType.FULL_TIME,
                'location': 'Bangalore, India',
                'salary_min': 1800000,
                'salary_max': 3000000,
                'experience': 2,
                'skills': 'Python, Django, FastAPI, Redis, PostgreSQL, Kafka, Docker',
                'description': (
                    'Build the algorithmic engine that routes delivery riders and optimizes dark store picking under strict 10-minute SLA.'
                ),
                'responsibilities': (
                    '- Design high-throughput microservices handling 500,000+ daily orders.\n'
                    '- Optimize real-time caching using Redis cluster.\n'
                    '- Collaborate directly with product leads and operations teams.'
                ),
            },
            {
                'title': 'Frontend Engineer (React & Mobile Web)',
                'job_type': Job.JobType.FULL_TIME,
                'location': 'Mumbai, India',
                'salary_min': 1600000,
                'salary_max': 2600000,
                'experience': 2,
                'skills': 'React, Next.js, TypeScript, Tailwind CSS, Redux Toolkit',
                'description': (
                    'Build lightning-fast, conversion-optimized web checkout and search experiences for millions of Zepto consumers.'
                ),
                'responsibilities': (
                    '- Build high-performance UI components with Next.js and React.\n'
                    '- Keep app bundle sizes small and achieve 95+ Lighthouse performance scores.'
                ),
            },
        ],
    },
    {
        'username': 'recruiter_cred',
        'email': 'careers@cred.club',
        'company_name': 'CRED',
        'company_type': Company.CompanyType.STARTUP,
        'website': 'https://cred.club/careers',
        'location': 'Bangalore, India',
        'industry': 'FinTech, High-Trust Payments & Rewards Ecosystem',
        'description': (
            'CRED is a members-only community celebrating creditworthy individuals. We build ultra-sleek, premium financial '
            'products spanning credit card bill payments, lending, wealth management, and peer-to-peer commerce.'
        ),
        'jobs': [
            {
                'title': 'Software Development Engineer - FinTech Systems',
                'job_type': Job.JobType.FULL_TIME,
                'location': 'Bangalore, India',
                'salary_min': 2500000,
                'salary_max': 4200000,
                'experience': 3,
                'skills': 'Python, Go, PostgreSQL, Redis, Microservices, System Design, Kafka',
                'description': (
                    'Design double-entry bookkeeping engines, automated payment settlements, and bank reconciliation pipelines.'
                ),
                'responsibilities': (
                    '- Build zero-downtime, fault-tolerant financial settlement services.\n'
                    '- Write clean, idiomatically correct backend code with 100% test coverage.\n'
                    '- Participate in architectural design discussions.'
                ),
            },
        ],
    },
    {
        'username': 'recruiter_blinkit',
        'email': 'careers@blinkit.com',
        'company_name': 'Blinkit',
        'company_type': Company.CompanyType.STARTUP,
        'website': 'https://blinkit.com/careers',
        'location': 'Gurgaon & Bangalore, India',
        'industry': 'Instant Commerce & Supply Chain Infrastructure',
        'description': (
            'Blinkit (an independent company within the Zomato group) is a pioneer of instant commerce in India, '
            'delivering over 10,000 products to doorsteps in 10 minutes.'
        ),
        'jobs': [
            {
                'title': 'Full Stack Developer (Python / React)',
                'job_type': Job.JobType.FULL_TIME,
                'location': 'Gurgaon, India',
                'salary_min': 1500000,
                'salary_max': 2500000,
                'experience': 2,
                'skills': 'Python, Django, React, TypeScript, PostgreSQL, Celery, Redis',
                'description': (
                    'Develop internal vendor management, inventory allocation, and store manager tooling across 800+ dark stores.'
                ),
                'responsibilities': (
                    '- Build responsive web applications used by thousands of store operators.\n'
                    '- Write asynchronous worker tasks in Celery for batch reconciliation.'
                ),
            },
        ],
    },
    {
        'username': 'recruiter_meesho',
        'email': 'careers@meesho.io',
        'company_name': 'Meesho',
        'company_type': Company.CompanyType.STARTUP,
        'website': 'https://meesho.io/careers',
        'location': 'Bangalore, India',
        'industry': 'Social Commerce & Small Business Marketplace',
        'description': (
            'Meesho is democratizing internet commerce for everyone in India. We empower millions of small sellers and '
            'home entrepreneurs to succeed online with 0% commission.'
        ),
        'jobs': [
            {
                'title': 'Backend Developer - Catalog & Search',
                'job_type': Job.JobType.FULL_TIME,
                'location': 'Bangalore, India (Hybrid)',
                'salary_min': 1600000,
                'salary_max': 2800000,
                'experience': 2,
                'skills': 'Python, Java, Elasticsearch, MySQL, Redis, AWS',
                'description': (
                    'Power multi-lingual search and personalized recommendation feeds for 100M+ monthly active buyers across Bharat.'
                ),
                'responsibilities': (
                    '- Build search indexing pipelines using Elasticsearch and Python.\n'
                    '- Implement ranking algorithms and A/B test experiments.'
                ),
            },
        ],
    },
    {
        'username': 'recruiter_razorpay',
        'email': 'careers@razorpay.com',
        'company_name': 'Razorpay',
        'company_type': Company.CompanyType.STARTUP,
        'website': 'https://razorpay.com/jobs/',
        'location': 'Bangalore, India',
        'industry': 'FinTech, Payments Infrastructure & Neo-Banking',
        'description': (
            'Razorpay is India’s first full-stack financial solutions company. We power payments for over 10 million '
            'businesses, enabling developers to integrate modern payment gateways, payroll, and banking in minutes.'
        ),
        'jobs': [
            {
                'title': 'Senior Python Backend Developer (Payments Engine)',
                'job_type': Job.JobType.FULL_TIME,
                'location': 'Bangalore, India (Hybrid)',
                'salary_min': 2200000,
                'salary_max': 3600000,
                'experience': 3,
                'skills': 'Python, Django, REST API, PostgreSQL, Redis, Docker, Microservices',
                'description': (
                    'Architect core payment routing and recurring subscription billing pipelines handling billions in monthly transaction volumes.'
                ),
                'responsibilities': (
                    '- Design and build resilient, PCI-DSS compliant payment microservices.\n'
                    '- Partner with banks and networks (Visa, Mastercard, UPI) for direct API integrations.\n'
                    '- Minimize API latencies and implement zero-data-loss failover mechanisms.'
                ),
            },
            {
                'title': 'Junior Python Developer (FinTech Tools)',
                'job_type': Job.JobType.FULL_TIME,
                'location': 'Bangalore, India',
                'salary_min': 900000,
                'salary_max': 1500000,
                'experience': 1,
                'skills': 'Python, Django, MySQL, REST API, Git, Postman',
                'description': (
                    'Build internal merchant verification, webhook monitoring, and dispute resolution dashboards.'
                ),
                'responsibilities': (
                    '- Implement secure webhooks and event streaming consumers.\n'
                    '- Assist merchant onboarding teams with automated KYC workflows.'
                ),
            },
        ],
    },
    {
        'username': 'recruiter_zerodha',
        'email': 'careers@zerodha.com',
        'company_name': 'Zerodha',
        'company_type': Company.CompanyType.STARTUP,
        'website': 'https://zerodha.com/careers',
        'location': 'Bangalore, India',
        'industry': 'Stock Broking, Trading Infrastructure & Open Source Tech',
        'description': (
            'Zerodha is India’s largest retail stock broker by active client base. Completely bootstrapped and profitable, '
            'Zerodha revolutionized the Indian broking industry with its discount pricing model and proprietary Kite trading engine.'
        ),
        'jobs': [
            {
                'title': 'Python & Systems Developer (Kite Platform)',
                'job_type': Job.JobType.FULL_TIME,
                'location': 'Bangalore, India',
                'salary_min': 1800000,
                'salary_max': 3200000,
                'experience': 2,
                'skills': 'Python, Go, PostgreSQL, Redis, Linux, WebSockets, Open Source',
                'description': (
                    'Join our tight-knit, engineering-first team building Kite, Coin, and Console. We love minimalistic code, '
                    'open-source software, and high-performance Unix architectures.'
                ),
                'responsibilities': (
                    '- Build real-time market data streaming services over WebSockets.\n'
                    '- Maintain clean codebases with zero unnecessary dependencies.\n'
                    '- Contribute to Zerodha open-source libraries and developer documentation.'
                ),
            },
        ],
    },

    # ==========================================
    # 4. MID-SIZED COMPANIES
    # ==========================================
    {
        'username': 'recruiter_freshworks',
        'email': 'careers@freshworks.com',
        'company_name': 'Freshworks',
        'company_type': Company.CompanyType.MID_SIZED,
        'website': 'https://www.freshworks.com/company/careers/',
        'location': 'Chennai & Bangalore, India',
        'industry': 'Customer Experience SaaS, CRM & ITSM Software',
        'description': (
            'Freshworks makes business software people love. Products like Freshdesk, Freshservice, and Freshsales '
            'enable over 60,000 businesses across the world to deliver delightful experiences to customers and employees.'
        ),
        'jobs': [
            {
                'title': 'Full Stack SaaS Engineer (Python / React)',
                'job_type': Job.JobType.FULL_TIME,
                'location': 'Chennai, India (Hybrid)',
                'salary_min': 1400000,
                'salary_max': 2400000,
                'experience': 2,
                'skills': 'Python, Django, React, AWS, MySQL, Redis, REST API',
                'description': (
                    'Develop multi-tenant cloud SaaS features for Freshservice IT service desk and automated ticketing workflows.'
                ),
                'responsibilities': (
                    '- Implement multi-tenant data isolation and scalable REST endpoints.\n'
                    '- Build modern React UI features with accessibility in mind.\n'
                    '- Conduct code reviews and unit test verifications.'
                ),
            },
        ],
    },
    {
        'username': 'recruiter_zoho',
        'email': 'careers@zoho.com',
        'company_name': 'Zoho Corporation',
        'company_type': Company.CompanyType.MID_SIZED,
        'website': 'https://www.zoho.com/careers/',
        'location': 'Chennai & Tenkasi, India',
        'industry': 'Cloud Software Suite & Business Operating System',
        'description': (
            'Zoho is a bootstrapped, privacy-first technology company providing a comprehensive suite of 55+ business applications '
            'spanning CRM, email, accounting, and HR to 100+ million users globally.'
        ),
        'jobs': [
            {
                'title': 'Software Developer (Python / Web Technologies)',
                'job_type': Job.JobType.FULL_TIME,
                'location': 'Chennai, India',
                'salary_min': 800000,
                'salary_max': 1500000,
                'experience': 1,
                'skills': 'Python, JavaScript, HTML5, CSS3, SQL, OOP, Algorithms',
                'description': (
                    'Build high-performance web modules and data analytics tools within the Zoho Office and CRM platforms.'
                ),
                'responsibilities': (
                    '- Write clean, efficient, and well-structured code in Python.\n'
                    '- Optimize relational database schemas and queries for large datasets.\n'
                    '- Work in a collaborative, long-term product engineering environment.'
                ),
            },
        ],
    },
    {
        'username': 'recruiter_thoughtworks',
        'email': 'careers@thoughtworks.com',
        'company_name': 'Thoughtworks',
        'company_type': Company.CompanyType.MID_SIZED,
        'website': 'https://www.thoughtworks.com/careers',
        'location': 'Pune, Bangalore, Hyderabad, India',
        'industry': 'Agile Software Consulting & Digital Innovation',
        'description': (
            'Thoughtworks is a leading global technology consultancy that integrates strategy, design, and software engineering '
            'to enable enterprises and technology disruptors to thrive as modern digital businesses.'
        ),
        'jobs': [
            {
                'title': 'Consultant Software Developer (Python / Clean Code)',
                'job_type': Job.JobType.FULL_TIME,
                'location': 'Pune, India (Hybrid)',
                'salary_min': 1500000,
                'salary_max': 2500000,
                'experience': 3,
                'skills': 'Python, TDD, Clean Architecture, Refactoring, CI/CD, Docker, PostgreSQL',
                'description': (
                    'Practice true Test-Driven Development (TDD), pair programming, and evolutionary architecture '
                    'building custom platforms for forward-thinking clients.'
                ),
                'responsibilities': (
                    '- Write unit, integration, and contract tests before writing production code.\n'
                    '- Facilitate technical workshops and design sessions with clients.\n'
                    '- Champion continuous delivery and automated deployment pipelines.'
                ),
            },
        ],
    },
    {
        'username': 'recruiter_persistent',
        'email': 'careers@persistent.com',
        'company_name': 'Persistent Systems',
        'company_type': Company.CompanyType.MID_SIZED,
        'website': 'https://www.persistent.com/careers/',
        'location': 'Pune & Hyderabad, India',
        'industry': 'Digital Engineering & Enterprise Modernization',
        'description': (
            'Persistent Systems is a trusted global digital engineering partner delivering technology solutions across '
            'banking, financial services, healthcare, and software product vendors.'
        ),
        'jobs': [
            {
                'title': 'Senior Python Developer (Cloud Microservices)',
                'job_type': Job.JobType.FULL_TIME,
                'location': 'Hyderabad, India',
                'salary_min': 1200000,
                'salary_max': 2000000,
                'experience': 4,
                'skills': 'Python, Django, AWS, Docker, Kubernetes, MySQL, Git',
                'description': (
                    'Develop scalable cloud microservices and modernize monolithic client applications into microservice architectures.'
                ),
                'responsibilities': (
                    '- Build REST APIs with comprehensive documentation.\n'
                    '- Containerize applications with Docker and deploy to Kubernetes.\n'
                    '- Ensure compliance with enterprise security protocols.'
                ),
            },
        ],
    },
    {
        'username': 'recruiter_browserstack',
        'email': 'careers@browserstack.com',
        'company_name': 'BrowserStack',
        'company_type': Company.CompanyType.MID_SIZED,
        'website': 'https://browserstack.wd3.myworkdayjobs.com/External',
        'location': 'Mumbai, India (Remote-First)',
        'industry': 'Software Testing Cloud & Developer Infrastructure',
        'description': (
            'BrowserStack is the world’s leading software testing platform powered by 15+ global data centers. '
            'Over 50,000 customers, including Microsoft, Twitter, and Spotify, rely on BrowserStack to deliver bug-free software. '
            'Core engineering roles (including backend, platform, and full stack) are listed under Software Engineer on their official Workday portal.'
        ),
        'jobs': [
            {
                'title': 'Software Engineer - Cloud Platform & Backend Systems',
                'job_type': Job.JobType.REMOTE,
                'location': 'Remote (India)',
                'salary_min': 2000000,
                'salary_max': 3400000,
                'experience': 2,
                'skills': 'Python, Linux, Docker, Distributed Systems, WebSockets, Redis, PostgreSQL, MySQL',
                'description': (
                    'Build distributed device clouds, backend services, and browser virtualization grids that run millions of automated tests daily. '
                    'Work on high-throughput backend infrastructure powering real-time testing across 3,000+ real mobile devices and desktop browsers.'
                ),
                'responsibilities': (
                    '- Architect and scale backend services powering cloud device grids.\n'
                    '- Manage real-time device allocation, containerization, and sandbox cleanup.\n'
                    '- Optimize network tunnels and streaming protocols for interactive browser sessions.'
                ),
            },
        ],
    },
    {
        'username': 'recruiter_zomato',
        'email': 'careers@zomato.com',
        'company_name': 'Zomato',
        'company_type': Company.CompanyType.MID_SIZED,
        'website': 'https://www.zomato.com/careers',
        'location': 'Gurgaon & Bangalore, India',
        'industry': 'Food Delivery, Restaurant Tech & Hyper-Local Marketplace',
        'description': (
            'Zomato is a technology platform that connects customers, restaurant partners, and delivery partners, '
            'serving their multiple needs across food ordering, dining out, and grocery essentials.'
        ),
        'jobs': [
            {
                'title': 'Full Stack Software Engineer (Python & React)',
                'job_type': Job.JobType.FULL_TIME,
                'location': 'Gurgaon, India',
                'salary_min': 1800000,
                'salary_max': 3000000,
                'experience': 2,
                'skills': 'Python, Django, React, TypeScript, PostgreSQL, Redis, AWS',
                'description': (
                    'Develop real-time restaurant management dashboards, automated kitchen display systems, and menu analytics.'
                ),
                'responsibilities': (
                    '- Build high-performance web applications in React and Django.\n'
                    '- Build low-latency microservices handling peak order rushes during lunch and dinner hours.\n'
                    '- Continuously monitor app health and optimize page load speeds.'
                ),
            },
        ],
    },
]


def run():
    today = timezone.now().date()
    now = timezone.now()
    created_count = 0
    updated_count = 0
    job_count = 0

    print("Starting Comprehensive Company & Job Seeding...")

    for comp_data in COMPANIES_DATA:
        username = comp_data['username']
        email = comp_data['email']
        cname = comp_data['company_name']
        ctype = comp_data['company_type']
        website = comp_data['website']
        location = comp_data['location']
        industry = comp_data['industry']
        desc = comp_data['description']
        jobs_list = comp_data['jobs']

        # 1. Get or create recruiter user
        user, u_created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': email,
                'first_name': f"{cname} Recruiter",
                'last_name': 'Team',
                'role': User.Role.RECRUITER,
                'is_staff': False,
            }
        )
        if u_created:
            user.set_password('password123')
            user.save()

        # 2. Get or create company
        company, c_created = Company.objects.get_or_create(
            recruiter=user,
            defaults={
                'name': cname,
                'company_type': ctype,
                'website': website,
                'location': location,
                'industry': industry,
                'description': desc,
                'is_approved': True,
            }
        )
        if not c_created:
            company.name = cname
            company.company_type = ctype
            company.website = website
            company.location = location
            company.industry = industry
            company.description = desc
            company.is_approved = True
            company.save()
            updated_count += 1
        else:
            created_count += 1

        # 3. Create or update jobs for this company
        for idx, jdata in enumerate(jobs_list):
            job_title = jdata['title']
            # Find or create job by company + title
            job, j_created = Job.objects.get_or_create(
                company=company,
                title=job_title,
                defaults={
                    'recruiter': user,
                    'job_type': jdata['job_type'],
                    'location': jdata['location'],
                    'salary_min': jdata['salary_min'],
                    'salary_max': jdata['salary_max'],
                    'experience_required_years': jdata['experience'],
                    'skills_required': jdata['skills'],
                    'description': jdata['description'],
                    'responsibilities': jdata.get('responsibilities', ''),
                    'deadline': today + timedelta(days=14 + ((idx * 2) % 16)),
                    'is_active': True,
                }
            )
            # Ensure fresh created_at time today
            job.recruiter = user
            job.job_type = jdata['job_type']
            job.location = jdata['location']
            job.salary_min = jdata['salary_min']
            job.salary_max = jdata['salary_max']
            job.experience_required_years = jdata['experience']
            job.skills_required = jdata['skills']
            job.description = jdata['description']
            job.responsibilities = jdata.get('responsibilities', '')
            job.deadline = today + timedelta(days=14 + ((idx * 2) % 16))
            job.is_active = True
            job.created_at = now - timedelta(hours=(idx * 2) + 1)
            job.save()
            job_count += 1

    print(f"Successfully processed {len(COMPANIES_DATA)} companies ({created_count} created, {updated_count} updated).")
    print(f"Total active jobs synced: {job_count}")

    # Ensure superuser and demo candidate exist for testing
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@careerpulse.com', 'admin123')
        print("Created superuser: admin / admin123")

    demo_cand, cand_created = User.objects.get_or_create(
        username='kavya',
        defaults={
            'email': 'kavya@careerpulse.com',
            'first_name': 'Kavya',
            'last_name': 'Candidate',
            'role': User.Role.CANDIDATE,
            'is_staff': False,
        }
    )
    if cand_created:
        demo_cand.set_password('password123')
        demo_cand.save()
        print("Created demo candidate: kavya / password123")


if __name__ == '__main__':
    run()
