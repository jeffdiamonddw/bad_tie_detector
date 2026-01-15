aws ecr get-login-password --region ca-central-1 | sudo docker login --username AWS --password-stdin 786487085471.dkr.ecr.ca-central-1.amazonaws.com
docker build -f docker/bad_tie_detector.dockerfile --platform linux/amd64 -t bad-tie-detector .
docker tag bad-tie-detector 786487085471.dkr.ecr.ca-central-1.amazonaws.com/bad-tie-detector:bad-tie-detector
sudo docker push 786487085471.dkr.ecr.ca-central-1.amazonaws.com/bad-tie-detector:bad-tie-detector

aws lambda delete-function --function-name bad-tie-detector

aws lambda create-function \
  --function-name bad-tie-detector \
  --package-type Image \
  --code ImageUri=786487085471.dkr.ecr.ca-central-1.amazonaws.com/bad-tie-detector:bad-tie-detector \
  --role arn:aws:iam::786487085471:role/tile-server \
  --timeout 900 \
  --memory-size 10240 \
  --ephemeral-storage Size=10240 \
  --region ca-central-1



