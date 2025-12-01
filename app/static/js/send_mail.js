<script>
document.getElementById("contactForm").addEventListener("submit", async function(e) {
    e.preventDefault();

    let form = e.target;
    let formData = new FormData(form);

    let response = await fetch("/send", {
        method: "POST",
        body: formData
    });

    let result = await response.json();
    let msgBox = document.getElementById("formResult");

    if (result.status === "ok") {
        msgBox.innerHTML = "<div class='alert alert-success'>Заявка отправлена!</div>";
        form.reset();
    } else {
        msgBox.innerHTML = "<div class='alert alert-danger'>Ошибка: " + result.error + "</div>";
    }
});
</script>
