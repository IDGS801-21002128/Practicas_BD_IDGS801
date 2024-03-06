function confirmarPedido(total) {
    // Obtener el precio total del pedido
    console.log("SIIII ENTRO")
    // Mostrar una alerta de confirmación con el precio del pedido
    var confirmacion = confirm("El precio total del pedido es: $" + total.toFixed(2) + ". ¿Desea confirmar el pedido?");
    
    // Si el usuario confirma el pedido, enviar el formulario
    if (confirmacion) {
        var formularioPedido = document.getElementById("formularioPedido");
        if (formularioPedido !== null) {
            formularioPedido.submit();
        }
    } else {
        // Si el usuario cancela el pedido, no hacer nada
    }
}
