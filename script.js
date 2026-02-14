// API Base URL
const API_URL = 'http://localhost:5000/api';

let clients = [];
let editingClientId = null;
let currentInteractionClientId = null;

// ==================== API FUNCTIONS ====================

async function fetchClients() {
    try {
        const response = await fetch(`${API_URL}/clients`);
        clients = await response.json();
        renderClients();
    } catch (error) {
        console.error('Error fetching clients:', error);
        alert('Failed to load clients. Make sure the server is running.');
    }
}

async function createClientAPI(clientData) {
    try {
        const response = await fetch(`${API_URL}/clients`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(clientData)
        });
        return await response.json();
    } catch (error) {
        console.error('Error creating client:', error);
        throw error;
    }
}

async function updateClientAPI(clientId, clientData) {
    try {
        const response = await fetch(`${API_URL}/clients/${clientId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(clientData)
        });
        return await response.json();
    } catch (error) {
        console.error('Error updating client:', error);
        throw error;
    }
}

async function deleteClientAPI(clientId) {
    try {
        const response = await fetch(`${API_URL}/clients/${clientId}`, {
            method: 'DELETE'
        });
        return await response.json();
    } catch (error) {
        console.error('Error deleting client:', error);
        throw error;
    }
}

async function createInteractionAPI(clientId, interactionData) {
    try {
        const response = await fetch(`${API_URL}/clients/${clientId}/interactions`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(interactionData)
        });
        return await response.json();
    } catch (error) {
        console.error('Error creating interaction:', error);
        throw error;
    }
}

// ==================== CLIENT FUNCTIONS ====================

async function addClient(e) {
    e.preventDefault();
    
    const clientData = {
        name: document.getElementById('clientName').value,
        company: document.getElementById('clientCompany').value,
        email: document.getElementById('clientEmail').value,
        phone: document.getElementById('clientPhone').value,
        amount: parseFloat(document.getElementById('clientAmount').value) || 0.0,
        status: document.getElementById('clientStatus').value,
        priority: document.getElementById('clientPriority').value
    };

    try {
        await createClientAPI(clientData);
        document.getElementById('clientForm').reset();
        await fetchClients();
    } catch (error) {
        alert('Failed to save client. Please try again.');
    }
}

function editClient(id) {
    const client = clients.find(c => c.id === id);
    if (!client) return;

    editingClientId = id;
    document.getElementById('editClientName').value = client.name;
    document.getElementById('editClientCompany').value = client.company || '';
    document.getElementById('editClientEmail').value = client.email;
    document.getElementById('editClientPhone').value = client.phone || '';
    document.getElementById('editClientAmount').value = client.amount || 0;
    document.getElementById('editClientStatus').value = client.status;
    document.getElementById('editClientPriority').value = client.priority;
    
    document.getElementById('editModal').classList.add('active');
}

function closeEditModal() {
    document.getElementById('editModal').classList.remove('active');
    document.getElementById('editClientForm').reset();
    editingClientId = null;
}

async function handleEditSubmit(e) {
    e.preventDefault();
    
    const clientData = {
        name: document.getElementById('editClientName').value,
        company: document.getElementById('editClientCompany').value,
        email: document.getElementById('editClientEmail').value,
        phone: document.getElementById('editClientPhone').value,
        amount: parseFloat(document.getElementById('editClientAmount').value) || 0.0,
        status: document.getElementById('editClientStatus').value,
        priority: document.getElementById('editClientPriority').value
    };

    try {
        await updateClientAPI(editingClientId, clientData);
        closeEditModal();
        await fetchClients();
    } catch (error) {
        alert('Failed to update client. Please try again.');
    }
}

async function deleteClient(id) {
    if (confirm('Are you sure you want to delete this client?')) {
        try {
            await deleteClientAPI(id);
            await fetchClients();
        } catch (error) {
            alert('Failed to delete client. Please try again.');
        }
    }
}

// ==================== INTERACTION FUNCTIONS ====================

function openInteractionModal(clientId) {
    currentInteractionClientId = clientId;
    document.getElementById('interactionDate').value = new Date().toISOString().split('T')[0];
    document.getElementById('interactionModal').classList.add('active');
}

function closeInteractionModal() {
    document.getElementById('interactionModal').classList.remove('active');
    document.getElementById('interactionForm').reset();
    currentInteractionClientId = null;
}

async function addInteraction(e) {
    e.preventDefault();
    
    const interactionData = {
        date: document.getElementById('interactionDate').value,
        type: document.getElementById('interactionType').value,
        notes: document.getElementById('interactionNotes').value
    };

    try {
        await createInteractionAPI(currentInteractionClientId, interactionData);
        closeInteractionModal();
        await fetchClients();
    } catch (error) {
        alert('Failed to save interaction. Please try again.');
    }
}

// ==================== FILTER & SORT FUNCTIONS ====================

function filterAndSortClients() {
    let filtered = [...clients];

    const statusFilter = document.getElementById('filterStatus').value;
    if (statusFilter !== 'all') {
        filtered = filtered.filter(c => c.status === statusFilter);
    }

    const priorityFilter = document.getElementById('filterPriority').value;
    if (priorityFilter !== 'all') {
        filtered = filtered.filter(c => c.priority === priorityFilter);
    }

    const searchTerm = document.getElementById('searchInput').value.toLowerCase();
    if (searchTerm) {
        filtered = filtered.filter(c => 
            c.name.toLowerCase().includes(searchTerm) ||
            (c.company && c.company.toLowerCase().includes(searchTerm)) ||
            c.email.toLowerCase().includes(searchTerm)
        );
    }

    const sortBy = document.getElementById('sortBy').value;
    switch(sortBy) {
        case 'date-desc':
            filtered.sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt));
            break;
        case 'date-asc':
            filtered.sort((a, b) => new Date(a.createdAt) - new Date(b.createdAt));
            break;
        case 'name-asc':
            filtered.sort((a, b) => a.name.localeCompare(b.name));
            break;
        case 'name-desc':
            filtered.sort((a, b) => b.name.localeCompare(a.name));
            break;
        case 'priority':
            const priorityOrder = { high: 3, medium: 2, low: 1 };
            filtered.sort((a, b) => priorityOrder[b.priority] - priorityOrder[a.priority]);
            break;
    }

    return filtered;
}

// ==================== RENDER FUNCTION ====================

function renderClients() {
    const clientsList = document.getElementById('clientsList');
    const filtered = filterAndSortClients();

    if (filtered.length === 0) {
        clientsList.innerHTML = `
            <div class="empty-state">
                <div class="empty-state-icon">📋</div>
                <h3>No clients found</h3>
                <p>Add your first client to get started!</p>
            </div>
        `;
        return;
    }

    clientsList.innerHTML = filtered.map(client => `
        <div class="client-card" onclick="event.stopPropagation()">
            <div class="client-header">
                <div>
                    <div class="client-name">
                        ${client.name}
                        <span class="priority-badge priority-${client.priority}">${client.priority.toUpperCase()}</span>
                        <span class="status-badge status-${client.status}">${client.status}</span>
                    </div>
                    ${client.company ? `<div class="client-company">${client.company}</div>` : ''}
                </div>
                <div class="card-actions">
                    <button class="action-icon log-icon" onclick="openInteractionModal(${client.id})" title="Log Interaction">
                        <i class="fa-solid fa-comment"></i>
                    </button>
                    <button class="action-icon edit-icon" onclick="editClient(${client.id})" title="Edit">
                        <i class="fa-solid fa-pen-to-square"></i>
                    </button>
                    <button class="action-icon delete-icon" onclick="deleteClient(${client.id})" title="Delete">
                        <i class="fa-solid fa-trash"></i>
                    </button>
                </div>
            </div>
            <div class="client-info">
                <div class="info-item">
                    <span class="info-label">📧 Email:</span> ${client.email}
                </div>
                ${client.phone ? `
                <div class="info-item">
                    <span class="info-label">📱 Phone:</span> ${client.phone}
                </div>
                ` : ''}
                <div class="info-item">
                    <span class="info-label">💰 Amount:</span> AED ${client.amount ? client.amount.toLocaleString('en-AE', {minimumFractionDigits: 2, maximumFractionDigits: 2}) : '0.00'}
                </div>
            </div>
            <div class="interactions">
                <div class="interactions-header">Recent Interactions (${client.interactions.length})</div>
                ${client.interactions.slice(-3).reverse().map(interaction => `
                    <div class="interaction-item">
                        <div class="interaction-date">
                            ${interaction.type === 'call' ? '📞' : interaction.type === 'email' ? '📧' : interaction.type === 'meeting' ? '🤝' : '📝'} 
                            ${new Date(interaction.date).toLocaleDateString()}
                        </div>
                        <div class="interaction-note">${interaction.notes}</div>
                    </div>
                `).join('') || '<div style="color: #999; font-size: 13px;">No interactions logged yet</div>'}
            </div>
        </div>
    `).join('');
}

// ==================== EVENT LISTENERS ====================

document.getElementById('clientForm').addEventListener('submit', addClient);
document.getElementById('editClientForm').addEventListener('submit', handleEditSubmit);
document.getElementById('interactionForm').addEventListener('submit', addInteraction);
document.getElementById('filterStatus').addEventListener('change', renderClients);
document.getElementById('filterPriority').addEventListener('change', renderClients);
document.getElementById('sortBy').addEventListener('change', renderClients);
document.getElementById('searchInput').addEventListener('input', renderClients);

document.getElementById('interactionModal').addEventListener('click', function(e) {
    if (e.target === this) {
        closeInteractionModal();
    }
});

document.getElementById('editModal').addEventListener('click', function(e) {
    if (e.target === this) {
        closeEditModal();
    }
});

// ==================== INITIALIZE ====================

// Load clients when page loads
fetchClients();