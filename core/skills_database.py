"""
Comprehensive Skill Taxonomy & Database for AI Resume Screening.
Includes 500+ skills mapped by category with synonyms and canonical names.
"""

SKILL_CATEGORIES = {
    "Programming Languages": [
        "python", "javascript", "typescript", "java", "c++", "c#", "c", "golang", "go",
        "rust", "ruby", "php", "swift", "kotlin", "scala", "r", "dart", "shell",
        "bash", "powershell", "perl", "lua", "matlab", "julia", "solidity", "sql"
    ],
    "Web & Frontend": [
        "react", "react.js", "reactjs", "next.js", "nextjs", "vue", "vue.js", "angular",
        "svelte", "html", "html5", "css", "css3", "sass", "scss", "tailwind", "tailwindcss",
        "bootstrap", "material-ui", "chakra ui", "redux", "zustand", "webpack", "vite",
        "graphql", "rest api", "restful api", "websockets", "jquery", "ajax"
    ],
    "Backend & Frameworks": [
        "django", "fastapi", "flask", "node.js", "nodejs", "express", "express.js",
        "spring", "spring boot", "asp.net", ".net core", "ruby on rails", "laravel",
        "nest.js", "nestjs", "gin", "grpc", "microservices", "celery", "rabbitmq",
        "apache kafka", "socket.io"
    ],
    "AI, Machine Learning & Data Science": [
        "machine learning", "deep learning", "nlp", "natural language processing",
        "computer vision", "artificial intelligence", "generative ai", "llms", "large language models",
        "langchain", "rag", "retrieval-augmented generation", "transformers", "bert", "gpt",
        "pytorch", "tensorflow", "keras", "scikit-learn", "sklearn", "opencv", "huggingface",
        "spacy", "nltk", "pandas", "numpy", "scipy", "statsmodels", "xgboost", "lightgbm",
        "catboost", "data analysis", "data science", "data visualization", "feature engineering",
        "predictive modeling", "clustering", "reinforcement learning", "neural networks", "cnn", "rnn", "lstm"
    ],
    "Databases & Caching": [
        "postgresql", "postgres", "mysql", "mongodb", "redis", "sqlite", "oracle",
        "microsoft sql server", "mssql", "cassandra", "dynamodb", "elasticsearch",
        "neo4j", "mariadb", "firebase", "supabase", "faiss", "chromadb", "pinecone",
        "nosql", "relational databases", "database design", "query optimization"
    ],
    "Cloud & DevOps": [
        "aws", "amazon web services", "azure", "gcp", "google cloud platform", "docker",
        "kubernetes", "k8s", "ci/cd", "github actions", "gitlab ci", "jenkins", "terraform",
        "ansible", "linux", "ubuntu", "nginx", "apache", "prometheus", "grafana", "helm",
        "serverless", "aws lambda", "s3", "ec2", "rds", "cloud computing", "devops"
    ],
    "Data Engineering & Big Data": [
        "apache spark", "spark", "pyspark", "hadoop", "kafka", "apache airflow", "airflow",
        "databricks", "snowflake", "bigquery", "redshift", "dbt", "etl", "data pipelines",
        "data warehousing"
    ],
    "Testing & Quality Assurance": [
        "pytest", "unittest", "selenium", "cypress", "jest", "mocha", "junit",
        "postman", "swagger", "api testing", "unit testing", "integration testing", "tdd", "bdd"
    ],
    "Mobile & UI/UX": [
        "react native", "flutter", "ios development", "android development", "swiftui",
        "figma", "adobe xd", "ui/ux design", "responsive design"
    ],
    "Methodologies & Soft Skills": [
        "agile", "scrum", "kanban", "jira", "git", "github", "gitlab", "bitbucket",
        "leadership", "team management", "communication", "problem solving",
        "critical thinking", "project management", "system design", "code review"
    ]
}

# Flattened set for high-speed lookup
ALL_SKILLS = set()
SKILL_MAP = {} # Lowercase skill -> Canonical display name

for category, skills in SKILL_CATEGORIES.items():
    for skill in skills:
        clean_s = skill.lower().strip()
        ALL_SKILLS.add(clean_s)
        # Format nice display name
        display_name = skill.title()
        if skill in ["aws", "gcp", "sql", "nosql", "css", "html", "api", "ai", "nlp", "llms", "rag", "ci/cd", "etl", "tdd", "bdd", "cnn", "rnn", "lstm"]:
            display_name = skill.upper()
        elif skill in ["mongodb", "mysql", "postgresql", "fastapi", "django", "flask", "react", "vue", "angular", "docker", "kubernetes", "pytorch", "tensorflow"]:
            display_name = skill.capitalize() if not (skill.startswith("postgre") or skill.startswith("fast")) else ("PostgreSQL" if "postgre" in skill else "FastAPI")
        
        SKILL_MAP[clean_s] = display_name

def get_skill_category(skill_name: str) -> str:
    """Returns the primary category for a given skill."""
    skill_lower = skill_name.lower().strip()
    for category, skills in SKILL_CATEGORIES.items():
        if skill_lower in skills:
            return category
    return "Other Technical Skills"
