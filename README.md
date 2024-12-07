![Install Dependencies](https://github.com/haobo-yuan/IDS706-FinalProject/actions/workflows/install.yml/badge.svg)
![Lint Code](https://github.com/haobo-yuan/IDS706-FinalProject/actions/workflows/lint.yml/badge.svg)
![Run Tests](https://github.com/haobo-yuan/IDS706-FinalProject/actions/workflows/test.yml/badge.svg)
![Format Code](https://github.com/haobo-yuan/IDS706-FinalProject/actions/workflows/format.yml/badge.svg)

# IDS706-FinalProject

## Quick View
Home Page:
![Home Screenshot](readme_components/Home.png)

Input Page:
![Input Screenshot](readme_components/Input.png)

Output Page:
![Output Screenshot](readme_components/Result.png)

## distroless
```bash
docker build -t your-app:latest .

docker run -p 8080:8080 your-app:latest
```
Access the application at:
> http://localhost:8080

docker build successfully:
![distroless Screenshot](readme_components/distroless_docker_build_successfully.png)
