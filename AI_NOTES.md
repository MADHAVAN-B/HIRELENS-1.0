# AI_NOTES

## What was AI-generated

I used AI assistance to generate the initial FastAPI project scaffold, API route structure, SQLAlchemy models, JWT authentication flow, Docker files, README, and test starter file.

## What I reviewed and changed

I reviewed the overall project structure, endpoint names, schema field names, and README workflow so the project matches the intended HireLens scope: resume analysis, candidate/job management, authentication, and matching.

## What I would validate manually

- End-to-end API testing through Swagger
- PostgreSQL connection and schema creation
- Resume upload behavior with real files
- Matching quality for real resumes and job descriptions
- Security and error-handling edge cases

## AI suggestions not fully relied on

The semantic matching logic currently uses a practical hybrid approach with skill overlap and optional SentenceTransformers embeddings. In a production system, I would tune the scoring logic further with real evaluation data instead of relying only on generated defaults.
