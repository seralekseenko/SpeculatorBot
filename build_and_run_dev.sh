#!/bin/bash

# Встановлюємо змінні
project_name="speculator_bot"
branch=$(git rev-parse --abbrev-ref HEAD)
commit_hash=$(git rev-parse HEAD)

# Перевіряємо, чи є незбережені зміни
if [ -n "$(git status --porcelain 2>/dev/null)" ]; then
    commit_hash="uncommitted"
fi

# Формуємо базовий тег
base_tag="${branch}_${commit_hash}"

# Знаходимо всі існуючі образи з таким же базовим тегом
existing_tags=$(docker images "$project_name" --format "{{.Tag}}" | grep "^${base_tag}_attempt[0-9]*$")

# Визначаємо наступний номер спроби
attempt_number=1
if [ -n "$existing_tags" ]; then
    max_attempt=0
    for tag in $existing_tags; do
        num=$(echo "$tag" | grep -oP 'attempt\K[0-9]+')
        if [ "$num" -gt "$max_attempt" ]; then
            max_attempt=$num
        fi
    done
    attempt_number=$((max_attempt + 1))
fi

# Повний тег образу
image_tag="${base_tag}_attempt${attempt_number}"

# Перевіряємо, чи існує образ з таким тегом
if docker images --format "{{.Repository}}:{{.Tag}}" | grep -q "^$project_name:$image_tag$"; then
    echo "Образ з тегом $image_tag вже існує. Переходимо до запуску контейнера."
else
    echo "Будуємо новий образ з тегом $image_tag."
    docker build -f Dockerfile.botTG -t "$project_name:$image_tag" -t "$project_name:latest" .
fi

# Встановлюємо ім'я для контейнера
container_name="${project_name}_container"

# Функція для очищення
cleanup() {
    # Зупиняємо роботу інших контейнерів цього проекту
    containers=$(docker ps --filter "ancestor=$project_name" -q)
    if [ -n "$containers" ]; then
        echo "Зупиняємо інші контейнери проекту $project_name."
        docker stop $containers
    fi

    # Зупиняємо поточний контейнер
    if [ "$(docker ps -q -f name="$container_name")" ]; then
        echo "Зупиняємо контейнер $container_name..."
        docker stop "$container_name"
    fi

    # Зупиняємо процес логування
    if [ -n "$logs_pid" ]; then
        kill "$logs_pid" 2>/dev/null
    fi
}

# Виконуємо початкове очищення
cleanup

# Запускаємо новий контейнер у фоновому режимі
docker run --rm -d --env-file .env --name "$container_name" "$project_name:$image_tag"

echo "Контейнер $container_name запущено у фоновому режимі."

# Запускаємо відображення логів у фоновому процесі
docker logs -f "$container_name" &
logs_pid=$!

# Обробляємо сигнали INT і TERM для коректного виходу
trap 'cleanup; exit 0' INT TERM

# Цикл для прийому команд від користувача
while true; do
    echo ""
    echo "Введіть 'stop', 'exit', 'quit' або 'terminate' для зупинки контейнера."
    echo ""
    read -r user_input
    case "$user_input" in
        stop|exit|quit|terminate)
            cleanup
            exit 0
            ;;
        *)
            echo "Невідома команда: $user_input"
            ;;
    esac
done
