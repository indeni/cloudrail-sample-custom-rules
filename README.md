# Sample Custom Rules for Cloudrail

[Cloudrail](https://www.indeni.com/cloudrail) is a product for scanning IaC (Terraform, etc) before, and during 
deployment, to catch security and other issues. The product has hundreds of rules built-in, but also allows users 
to write and execute their own sets of rules.

To support this, there's a publicly available Python package called 
[cloudrail-knowledge](https://github.com/indeni/cloudrail-knowledge). We suggest you read the documentation there before
continuing here.

This repository showcases examples of custom rules that can be written using that package, and how to use them together 
with Cloudrail. We've also prepared a short video on how to write your own rules, 
[take a look](https://youtu.be/MQfpKDQAW8o).

## How should I use this repository with Cloudrail?

Prerequisities:
* Cloudrail account
* A preferred way to run it (like via Docker locally, or in CI)

Then, using this repository, is simply a matter of cloning it locally, and passing the directory as a parameter:
```
git clone https://github.com/indeni/cloudrail-sample-custom-rules
docker run --rm -it -v $PWD:/data -v cloudrail:/indeni indeni/cloudrail-cli run -p plan.out -v --custom-rules cloudrail-sample-custom-rules/src
```

Notice a couple of flags in the command that aren't normally used:
* `-v` (the one just before `--custom-rules`) - this flag is used to show the results even if the rule is set to Advise. This is useful while you're still 
  testing your rules.
  
* `--custom-rules` - this provides a directory from where Cloudrail should load the custom rules' code.

*IMPORTANT:* When using Cloudrail in a docker container (as in the example above), the Cloudrail CLI code can only 
access content that has been mounted via Docker's `-v` flag. In the above example, we use `-v $PWD:/data`. This means
that the custom rules' code must be in a subdirectory of where we run this command. If it's anywhere else, the code 
within the Docker container won't be able to access it.

## How can I try out the rules here on my own?

To see how these rules work against a Terraform example code, follow these steps:
1. Clone this repository.
2. Run a `terraform init` and `terraform plan -out=plan.out` in the sub-directory `tf-test-cases`, like so:
```
terraform -chdir=tf-test-cases init
terraform -chdir=tf-test-cases plan -out=plan.out
```
3. Run Cloudrail with the custom rules:
```
docker run --rm -it -v $PWD:/data -v cloudrail:/indeni indeni/cloudrail-cli run -p tf-test-cases/plan.out -v --custom-rules ./src
```
4. And see the result:
```
✔ Reading custom rules...
✔ Preparing a filtered Terraform plan locally before uploading to Cloudrail Service...
✔ Re-running your Terraform plan through a customized 'terraform plan' to generate needed context data...
✔ Filtering and processing Terraform data...
✔ Obfuscating IP addresses...
< removed filtered content from brevity >
✔ Submitting Terraform data to the Cloudrail Service...
✔ Your job id is: 076a37b5-6b1e-4a21-a9cc-965cd45d90e8
✔ Cloudrail Service accessing the latest cached snapshot of cloud account 154724799477. Timestamp: 2021-05-13 21:27:23Z...
✔ Building simulated graph model, representing how the cloud account will look like if the plan were to be applied...
✔ Running context-aware rules...
✔ Running custom rules...
✔ Returning results, almost done!
✔ Assessment complete, fetching results...

WARNINGs found:
Rule: Ensure only approved third party accounts can assume roles
 - 1 Resources Exposed:
-----------------------------------------------
   - Exposed Resource: [aws_iam_role.unapproved_third_party] (role_with_unapproved_third_party.tf:5)
     Violating Resource: [aws_iam_role.unapproved_third_party]  (role_with_unapproved_third_party.tf:5)

     Evidence:
             | The IAM role aws_iam_role.unapproved_third_party has a trust policy that allows account 111122223333 to assume it but that is not in the list of pre-approved third-party accounts

...
```