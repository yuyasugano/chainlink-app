# Chainlink Application with AWS SAM

An application is an Web API that Chainlink node and job can call for and retrieves information from Web API. It is an `AWS SAM` application with a smartcontract written in solidity. External Adapters integration is TBD.
 
## Terraform References
  - [Terraform Module Registry](https://registry.terraform.io/)
  - [Terraform Structure Best Practices](https://dev.classmethod.jp/devops/directory-layout-bestpractice-in-terraform/)
  - [Terraform Best Practices in 2017](https://qiita.com/shogomuranushi/items/e2f3ff3cfdcacdd17f99)
  - [shogomuranushi/oreno-terraform](https://github.com/shogomuranushi/oreno-terraform)
 
### Deploy DynamoDB Build
- move to main directory and run
```
cd main
 
terraform init
terraform plan # confirm
terraform apply # run
 
terraform destroy # destroy
```
 
## sam version

Ensure your `sam` version is as follows (some modifications would be required if you run other `sam` versions):
```sh
$ pip install aws-sam-cli
$ sam --version
SAM CLI, version 0.48.0
```
To install `aws-sam-cli`, visit https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html
  
## environment variables

vars.json
```
{
  "IngestApplication": {
    "TABLE_NAME": "chainlink"
  }
}
```
  
## setup steps
 
1. Prepare S3 bucket to upload the code and generate a compiled version of the template `compiled.yml`. You need to manually create an S3 bucket or use an existing one to store the code.
2. Install the external libraries for new Lambda function. The libraries need to be in the same directory and S3 location.
2. Compile `template.yml` and generate a compiled version of the template `compiled.yml` with `sam package`command
3. Submit the compiled template to CloudFormation and deploy your serverless application with `sam deploy`command as follows 
 
```sh
cd ingest_sam/
aws s3 mb s3://<Your S3 bucket> --region <Your region>
sam validate -t template.yaml
sam package --template-file template.yaml --s3-bucket <Your S3 bucket> --output-template-file compiled.yaml
sam deploy --template-file compiled.yaml --stack-name <Your stack name> --capabilities CAPABILITY_IAM --parameter-overrides TableName=<TABLE_NAME>
```
 
## local test
```sh
sam local invoke IngestApplication --event event.json --region ap-northeast-1 --env-vars vars.json
```
  
## License

This library is licensed under the MIT License.
