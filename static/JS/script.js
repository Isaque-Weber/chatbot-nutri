// ---------------------------------------------------
//  SEÇÃO 1: Lógica de abrir/fechar modais
// ---------------------------------------------------

// Abre o modal de cadastro
function openAddModal() {
    document.getElementById('addModal').style.display = 'block';
}

// Fecha o modal de cadastro
function closeAddModal() {
    document.getElementById('addModal').style.display = 'none';
}

// Abre o modal de edição, preenchendo campos
function openEditModal(id, nome, telefone, autorizado, has_comorbidity) {
    // Preenche os inputs do modal de edição
    document.getElementById('edit_id').value = id;
    document.getElementById('edit_nome').value = nome;
    document.getElementById('edit_telefone').value = telefone;
    document.getElementById('edit_autorizado').value = autorizado;
    document.getElementById('edit_comorbidity').value = has_comorbidity;

    document.getElementById('editModal').style.display = 'block';
}

// Fecha o modal de edição
function closeEditModal() {
    document.getElementById('editModal').style.display = 'none';
}

// Fecha os modais se o usuário clicar fora do conteúdo
window.onclick = function (event) {
    const addM = document.getElementById('addModal');
    const editM = document.getElementById('editModal');

    if (event.target === addM) {
        addM.style.display = 'none';
    }
    if (event.target === editM) {
        editM.style.display = 'none';
    }
};

// ---------------------------------------------------
//  SEÇÃO 2: Lógica de CRUD via Fetch API (opcional)
// ---------------------------------------------------

// Exemplo de função para carregar usuários dinamicamente
async function loadUsers() {
    try {
        const response = await fetch('/api/usuarios');  // Ajuste a rota conforme sua API
        const data = await response.json();

        // Supondo que você tenha uma <tbody> com id="user-list" no HTML
        const userList = document.getElementById('user-list');
        userList.innerHTML = ''; // limpa

        data.forEach(user => {
            const row = document.createElement('tr');
            row.innerHTML = `
        <td>${user.id}</td>
        <td>${user.nome}</td>
        <td>${user.telefone}</td>
        <td>${user.autorizado ? 'Sim' : 'Não'}</td>
        <td>${user.has_comorbidity ? 'Sim' : 'Não'}</td>
        <td>
        <button onclick="editUser(${user.id})">Editar</button>
        <button onclick="deleteUser(${user.id})">Excluir</button>
        </td>
    `;
            userList.appendChild(row);
        });
    } catch (error) {
        console.error('Erro ao carregar usuários:', error);
        alert('Erro ao carregar usuários.');
    }
}

// Exemplo de função para editar um usuário via modal
async function editUser(id) {
    // 1) Busca dados do usuário na API
    try {
        const response = await fetch(`/api/usuarios/${id}`);
        const user = await response.json();

        // 2) Preenche o modal com os dados
        document.getElementById('edit_id').value = user.id;
        document.getElementById('edit_nome').value = user.nome;
        document.getElementById('edit_telefone').value = user.telefone;
        document.getElementById('edit_autorizado').value = user.autorizado ? '1' : '0';
        document.getElementById('edit_comorbidity').value = user.has_comorbidity ? '1' : '0';

        // 3) Abre o modal
        document.getElementById('editModal').style.display = 'block';
    } catch (error) {
        console.error('Erro ao carregar usuário:', error);
        alert('Erro ao carregar usuário.');
    }
}

// Exemplo de função para excluir usuário
async function deleteUser(id) {
    if (!confirm('Tem certeza que deseja excluir este usuário?')) return;

    try {
        const response = await fetch(`/api/usuarios/${id}`, { method: 'DELETE' });
        if (response.ok) {
            alert('Usuário excluído com sucesso!');
            loadUsers(); // recarrega a lista
        } else {
            alert('Erro ao excluir usuário.');
        }
    } catch (error) {
        console.error('Erro ao excluir usuário:', error);
        alert('Erro ao excluir usuário.');
    }
}

// Exemplo de função para criar usuário (chamada no modal de cadastro)
async function createUser() {
    const nome = document.getElementById('add_nome').value;
    const telefone = document.getElementById('add_telefone').value;
    const hasComorbidity = document.getElementById('add_comorbidity').value;
    const autorizado = document.getElementById('add_autorizado').value;

    const userData = {
        nome: nome,
        telefone: telefone,
        has_comorbidity: hasComorbidity === '1' ? 1 : 0,
        autorizado: autorizado === '1' ? 1 : 0
    };

    try {
        const response = await fetch('/api/usuarios', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(userData)
        });
        if (response.ok) {
            alert('Usuário criado com sucesso!');
            closeAddModal();
            loadUsers(); // recarrega a lista
        } else {
            alert('Erro ao criar usuário.');
        }
    } catch (error) {
        console.error('Erro ao criar usuário:', error);
        alert('Erro ao criar usuário.');
    }
}

// Se quiser carregar a lista assim que a página abrir (modo SPA):
document.addEventListener('DOMContentLoaded', () => {
    // loadUsers();  // Descomente se quiser usar a lista dinâmica
});  