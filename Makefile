# ----------------------------------
#          INSTALL & TEST
# ----------------------------------
install_requirements:
	@pip install -r requirements.txt

check_code:
	@flake8 scripts/* Voight-Kampff-Test-Backend/*.py

black:
	@black scripts/* Voight-Kampff-Test-Backend/*.py

test:
	@coverage run -m pytest tests/*.py
	@coverage report -m --omit="${VIRTUAL_ENV}/lib/python*"

ftest:
	@Write me

clean:
	@rm -f */version.txt
	@rm -f .coverage
	@rm -fr */__pycache__ */*.pyc __pycache__
	@rm -fr build dist
	@rm -fr Voight-Kampff-Test-Backend-*.dist-info
	@rm -fr Voight-Kampff-Test-Backend.egg-info

install:
	@pip install . -U

all: clean install test black check_code

count_lines:
	@find ./ -name '*.py' -exec  wc -l {} \; | sort -n| awk \
        '{printf "%4s %s\n", $$1, $$2}{s+=$$0}END{print s}'
	@echo ''
	@find ./scripts -name '*-*' -exec  wc -l {} \; | sort -n| awk \
		        '{printf "%4s %s\n", $$1, $$2}{s+=$$0}END{print s}'
	@echo ''
	@find ./tests -name '*.py' -exec  wc -l {} \; | sort -n| awk \
        '{printf "%4s %s\n", $$1, $$2}{s+=$$0}END{print s}'
	@echo ''

# ----------------------------------
#      UPLOAD PACKAGE TO PYPI
# ----------------------------------
PYPI_USERNAME=<AUTHOR>
build:
	@python setup.py sdist bdist_wheel

pypi_test:
	@twine upload -r testpypi dist/* -u $(PYPI_USERNAME)

pypi:
	@twine upload dist/* -u $(PYPI_USERNAME)

run_api:
	uvicorn api.fast:app --reload


# ----------------------------------
#      GCP INFO
# ----------------------------------

PROJECT_ID=wagon-bootcamp-354400

BUCKET_NAME=voight-kampff-test

REGION=	US-WEST1

set_project:
	@gcloud config set project ${PROJECT_ID}

create_bucket:
	@gsutil mb -l ${REGION} -p ${PROJECT_ID} gs://${BUCKET_NAME}

LOCAL_PATH='What's_a_weird_smell_you're_willing_to_admit_you_like_all.csv'

BUCKET_FOLDER=raw_data

BUCKET_FILE_NAME=$(shell basename ${LOCAL_PATH})

BUCKET_TRAINING_FOLDER = 'trainings'

PYTHON_VERSION=3.8.12
RUNTIME_VERSION=1.15

PACKAGE_NAME=VoightKampffModel
FILENAME=response_generator

JOB_NAME=ai_response_training_$(shell date +'%Y%m%d_%H%M%S')

upload_data:
    # @gsutil cp train_1k.csv gs://wagon-ml-my-bucket-name/data/train_1k.csv
	@gsutil cp ${LOCAL_PATH} gs://${BUCKET_NAME}/${BUCKET_FOLDER}/${BUCKET_FILE_NAME}

gcp_submit_training:
	@gcloud ai-platform jobs submit training ${JOB_NAME} \
		--job-dir gs://${BUCKET_NAME}/${BUCKET_TRAINING_FOLDER} \
		--package-path ${PACKAGE_NAME} \
		--module-name ${PACKAGE_NAME}.${FILENAME} \
		--python-version=${PYTHON_VERSION} \
		--runtime-version=${RUNTIME_VERSION} \
		--region ${REGION} \
		--scale-tier CUSTOM \
    --master-machine-type n1-standard-16 \
		--stream-logs
