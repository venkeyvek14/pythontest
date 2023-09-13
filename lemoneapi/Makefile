NAME:=lemone-backend
DOCKER_REPOSITORY:=<your_docker_repository>
DOCKER_IMAGE_NAME:=$(DOCKER_REPOSITORY)/$(NAME)
VERSION:=0.1.0

.PHONY: build clean test build-container push-container test-container

build :
	python3 manage.py

clean :
	@echo ""

test:
	#@pytest
	python3 manage.py &
	sleep 5
	# pytest
	# add commands

build-container :
	@docker build --platform linux/amd64 -t $(DOCKER_IMAGE_NAME):$(VERSION) .

push-container :
	@docker push $(DOCKER_IMAGE_NAME):$(VERSION)

test-container :
	@docker rm -f $(NAME) || true
	# python server is running a 8000, map to docker 8000
	@docker run --platform linux/amd64 -dp 8000:8000 --name=$(NAME) $(DOCKER_IMAGE_NAME):$(VERSION)
	@docker ps
	@sleep 5
	@echo "add test commands"
	@echo ""
	@sleep 2
	@docker stop $(NAME) || true
	@docker rm -f $(NAME) || true