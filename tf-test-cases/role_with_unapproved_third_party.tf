resource "aws_iam_role" "unapproved_third_party" {
  name = "unapproved_third_party"
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "",
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    },
    {
      "Sid": "",
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::111122223333:user/LiJuan"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF

}
