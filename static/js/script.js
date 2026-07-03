function preencherPagamento(select) {
  const opt = select.options[select.selectedIndex];
  const cliente = opt.getAttribute('data-cliente');
  const valor = opt.getAttribute('data-valor');
  if (cliente) {
    document.getElementById('input-cliente').value = cliente;
    document.getElementById('input-valor').value = valor;
  }
}
document.addEventListener('click', function(e) {
  if (e.target.classList.contains('modal')) e.target.classList.remove('show');
});
document.addEventListener('DOMContentLoaded', function() {
  const hoje = new Date().toISOString().split('T')[0];
  document.querySelectorAll('input[type="date"]').forEach(i => { if (!i.value) i.value = hoje; });
});
