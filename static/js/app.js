function abrirModalEliminar(idProducto) {
    Swal.fire({
        title: 'Eliminar Producto',
        text: "¿Está seguro de eliminar?",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        cancelButtonText: 'NO',
        confirmButtonText: 'SI'
    }).then((result) => {
        if (result.isConfirmed) {
            location.href = "/eliminar/" + idProducto;
        }
    });
}