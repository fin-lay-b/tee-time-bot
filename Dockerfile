FROM public.ecr.aws/lambda/python:3.12

COPY zscaler-root-ca.crt ${LAMBDA_TASK_ROOT}/cert.crt

ENV SSL_CERT_FILE=${LAMBDA_TASK_ROOT}/cert.crt
ENV REQUESTS_CA_BUNDLE=${LAMBDA_TASK_ROOT}/cert.crt
ENV CURL_CA_BUNDLE=${LAMBDA_TASK_ROOT}/cert.crt


COPY requirements.txt ${LAMBDA_TASK_ROOT}
RUN pip install -r requirements.txt

# Copy the lambda function code
COPY lambda_function.py ${LAMBDA_TASK_ROOT}
COPY aws/ ${LAMBDA_TASK_ROOT}/aws/
COPY wc_gc/ ${LAMBDA_TASK_ROOT}/wc_gc/

# Set the handler
CMD [ "lambda_function.lambda_handler" ]