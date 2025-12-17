
document.addEventListener('DOMContentLoaded', function() {
    console.log('Каталог товаров загружен!');

    const deleteButtons = document.querySelectorAll('.btn-delete');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm('Вы уверены, что хотите удалить этот товар?')) {
                e.preventDefault();
            }
        });
    });
});