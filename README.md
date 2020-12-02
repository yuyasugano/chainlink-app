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
 
  
## License

This library is licensed under the MIT License.
