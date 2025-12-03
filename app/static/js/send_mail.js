document.getElementById("contactForm").addEventListener("submit", async function(e) {
    e.preventDefault();

    let form = e.target;
    let formData = new FormData(form);
    let msgBox = document.getElementById("formResult");

    try {
        let response = await fetch("/send", {
            method: "POST",
            body: formData
        });

        // Получаем ответ всегда как текст
        let raw = await response.text();
        console.log("RAW RESPONSE:", raw);

        let result;

        try {
            // Пытаемся парсить как JSON
            result = JSON.parse(raw);
        } catch (err) {
            // Если не JSON — покажем текст ответа
            msgBox.innerHTML = `
                <div class="alert alert-danger">
                    Сервер вернул не JSON:<br>
                    <pre>${raw}</pre>
                </div>`;
            return;
        }

        // Если JSON нормальный
        if (result.status === "ok") {
            msgBox.innerHTML = "<div class='alert alert-success'>Заявка отправлена!</div>";
            form.reset();
        } else {
            msgBox.innerHTML = "<div class='alert alert-danger'>Ошибка: " + result.error + "</div>";
        }

    } catch (e) {
        msgBox.innerHTML = `
            <div class="alert alert-danger">
                JS ошибка: ${e.message}
            </div>`;
    }
});
