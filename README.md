# Sample Custom Rules for Cloudrail

[Cloudrail](https://www.indeni.com/cloudrail) is a product for scanning IaC (Terraform etc) before, and during deployment, to catch security and other issues. The product has hundreds of rules built-in, but also allows users to write and execute their own sets of rules.

To support this, there's a publicly available Python package called [cloudrail-knowledge](https://github.com/indeni/cloudrail-knowledge).

This repository showcases examples of custom rules that can be written using that package, and how to use them together with Cloudrail.