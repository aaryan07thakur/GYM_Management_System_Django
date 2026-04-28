
document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".delete-form").forEach(form => {
        form.addEventListener("submit", function (e) {
            if (!confirm("Are you sure you want to delete?")) {
                e.preventDefault();
            }
        });
    });
});