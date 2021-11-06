resource "aws_iam_role" "role_lambda" {
  name = "role_lambda"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_lambda_function" "lambda_solaredge_deviation" {
  filename      = "../solarEdgeGeneric/my-deployment-package.zip"
  function_name = "lambda_function.py"
  role          = aws_iam_role.role_lambda.arn
  handler       = "lambda_handler"
  source_code_hash = filebase64sha256("../solarEdgeGeneric/my-deployment-package.zip")
  runtime = "python3.8"
  timeout     = 3
  memory_size = 128

  environment {
    variables = {
      foo = "bar"
    }
  }
}
