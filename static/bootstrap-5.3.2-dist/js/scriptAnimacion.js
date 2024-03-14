document.addEventListener("DOMContentLoaded", function() {
    const confirmarTerminarBtn = document.getElementById("confirmarTerminarBtn");
    if (confirmarTerminarBtn) {
        confirmarTerminarBtn.addEventListener("click", function() {
            if (confirm("¿Estás seguro de que deseas terminar este pedido?")) {
                document.getElementById("terminarForm").submit();
            }
        });
    }
});