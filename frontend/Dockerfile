FROM node:24-alpine

WORKDIR /app

# 의존성 설치
COPY package.json package-lock.json ./
RUN npm ci

# 애플리케이션 코드 복사
COPY . .

# 포트 노출
EXPOSE 3000

# 실행 명령
CMD ["npm", "run", "dev"]
