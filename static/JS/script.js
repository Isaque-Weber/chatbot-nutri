// Função para abrir o modal
function openModal() {
    document.getElementById('user-modal').style.display = 'block';
}

// Função para fechar o modal
function closeModal() {
    document.getElementById('user-modal').style.display = 'none';
}

// Função para salvar o usuário
async function saveUser() {
    const phone = document.getElementById('user-phone').value;
    const hasComorbidity = document.getElementById('has-comorbidity').value;

    const user = {
        telefone: phone,
        comorbidade: hasComorbidity === '1'
    };

    try {
        const response = await fetch('/api/usuarios', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(user)
        });

        if (response.ok) {
            alert('Usuário salvo com sucesso!');
            closeModal();
            loadUsers(); // Recarrega a lista de usuários
        } else {
            alert('Erro ao salvar usuário.');
        }
    } catch (error) {
        console.error('Erro:', error);
        alert('Erro ao salvar usuário.');
    }
}

// Função para carregar a lista de usuários
async function loadUsers() {
    try {
        const response = await fetch('/api/usuarios');
        const users = await response.json();

        const userList = document.getElementById('user-list');
        userList.innerHTML = '';

        users.forEach(user => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${user.id}</td>
                <td>${user.telefone}</td>
                <td>
                    <button onclick="editUser(${user.id})">Editar</button>
                    <button onclick="deleteUser(${user.id})">Excluir</button>
                </td>
            `;
            userList.appendChild(row);
        });
    } catch (error) {
        console.error('Erro:', error);
        alert('Erro ao carregar usuários.');
    }
}

// Função para editar um usuário
async function editUser(id) {
    try {
        const response = await fetch(`/api/usuarios/${id}`);
        const user = await response.json();

        document.getElementById('user-phone').value = user.telefone;
        document.getElementById('has-comorbidity').value = user.comorbidade ? '1' : '0';

        openModal();
    } catch (error) {
        console.error('Erro:', error);
        alert('Erro ao carregar usuário.');
    }
}

// Função para excluir um usuário
async function deleteUser(id) {
    if (!confirm('Tem certeza que deseja excluir este usuário?')) {
        return;
    }

    try {
        const response = await fetch(`/api/usuarios/${id}`, {
            method: 'DELETE'
        });

        if (response.ok) {
            alert('Usuário excluído com sucesso!');
            loadUsers(); // Recarrega a lista de usuários
        } else {
            alert('Erro ao excluir usuário.');
        }
    } catch (error) {
        console.error('Erro:', error);
        alert('Erro ao excluir usuário.');
    }
}
// --- MODAL DE CADASTRO ---
function openAddModal() {
    document.getElementById('addModal').style.display = 'block';
  }
  function closeAddModal() {
    document.getElementById('addModal').style.display = 'none';
  }

  // --- MODAL DE EDIÇÃO ---
  function openEditModal(id, nome, telefone, autorizado, has_comorbidity) {
    // Preenche os campos do form
    document.getElementById('edit_id').value = id;
    document.getElementById('edit_nome').value = nome;
    document.getElementById('edit_telefone').value = telefone;
    document.getElementById('edit_comorbidity').value = has_comorbidity;
    document.getElementById('edit_autorizado').value = autorizado;

    // Abre o modal
    document.getElementById('editModal').style.display = 'block';
  }
  function closeEditModal() {
    document.getElementById('editModal').style.display = 'none';
  }

  // Fecha modais se clicar fora do conteúdo
  window.onclick = function(event) {
    let addM = document.getElementById('addModal');
    let editM = document.getElementById('editModal');
    if (event.target == addM) {
      addM.style.display = 'none';
    }
    if (event.target == editM) {
      editM.style.display = 'none';
    }
  }
// Carrega a lista de usuários ao carregar a página
document.addEventListener('DOMContentLoaded', loadUsers);