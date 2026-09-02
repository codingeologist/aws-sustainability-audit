# AWS Account Emissions Report

This repo utilises the [AWS CLI](https://aws.amazon.com/cli/) and [AWS SDK](https://docs.aws.amazon.com/boto3/latest/) to create an emissions report of all AWS accounts used in an organisation.

Install dependencies:
```bash
uv venv venv
uv pip install boto3 pandas duckdb matplotlib streamlit
```

Export AWS emissions data for every Account with:
```bash
# This assumes all AWS account profiles are stored within the ~/.aws/config file
export AWS_PROFILE=[profile-name] && aws sso login && python3 main.py
```

Run the Streamlit app with:
```bash
streamlit run streamlit_app.py
```

This repo is a work in progress watch this space 👁😜