#!/bin/bash
cat <<EOF > message.json
a
b
c
EOF
cat <<EOF > destination.json
{
  "ToAddresses":  ["sunjoo.park@nota.ai"],
  "CcAddresses":  [],
  "BccAddresses": []
}
EOF
cat <<EOF > message.json
{
    "Subject": {
        "Data": "Test email sent using the AWS CLI",
        "Charset": "UTF-8"
    },
    "Body": {
        "Text": {
            "Data": "This is the message body in text format.",
            "Charset": "UTF-8"
        },
        "Html": {
            "Data": "This message body contains HTML formatting. It can, for example, contain links like this one: <a class=\"ulink\" href=\"http://docs.aws.amazon.com/ses/latest/DeveloperGuide\" target=\"_blank\">Amazon SES Developer Guide</a>.",
            "Charset": "UTF-8"
        }
    }
}
EOF
aws ses send-email --from netspresso@nota.ai --destination file://destination.json --message file://message.json

#aws ses send-email --text='test_message' --from netspresso@nota.ai --to sunjoo.park@nota.ai --subject "test message"