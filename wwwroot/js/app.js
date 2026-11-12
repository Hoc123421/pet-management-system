/* ==========================================================================
   PETCARE HUB - CLIENT JAVASCRIPT APPLICATION
   ========================================================================== */

const API_BASE = '/api';

// Global Application State
const state = {
  currentUser: JSON.parse(localStorage.getItem('currentUser')) || null,
  authToken: localStorage.getItem('authToken') || null,
  theme: localStorage.getItem('theme') || 'light',
  
  // Pet Catalog State
  pets: {
    page: 1,
    pageSize: 6,
    search: '',
    species: 'Tất cả',
    gender: 'Tất cả',
    sortBy: 'newest',
    totalPages: 1,
    items: []
  },

  // Products State
  products: {
    page: 1,
    pageSize: 8,
    search: '',
    category: 'Tất cả',
    sortBy: 'newest',
    totalPages: 1,
    items: []
  },

  // Cart State (Loaded per account)
  cart: []
};

// Initialize Application
document.addEventListener('DOMContentLoaded', () => {
  initTheme();
  updateAuthUI();
  setupEventListeners();
  initGoogleOAuth();
  loadUserCart();



  
  // Initial Data Loads
  loadPets();
  loadServices();
  loadProducts();
  if (state.currentUser) {
    loadMyAppointments();
    if (state.currentUser.role === 'Admin') {
      loadAdminDashboard();
    }
  }
});

/* ==========================================================================
   THEME SWITCHER
   ========================================================================== */
function initTheme() {
  document.documentElement.setAttribute('data-theme', state.theme);
  const themeBtnIcon = document.querySelector('#themeToggle i');
  if (themeBtnIcon) {
    themeBtnIcon.className = state.theme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
  }
}

function toggleTheme() {
  state.theme = state.theme === 'light' ? 'dark' : 'light';
  localStorage.setItem('theme', state.theme);
  initTheme();
  showToast(`Đã chuyển sang chế độ ${state.theme === 'dark' ? 'Giao diện Tối' : 'Giao diện Sáng'}`);
}

/* ==========================================================================
   NAVIGATION & SECTION SWITCHER
   ========================================================================== */
function switchTab(sectionId) {
  const mainContent = document.getElementById('mainContent');
  const adminSection = document.getElementById('adminSection');

  if (sectionId === 'adminSection') {
    if (mainContent) mainContent.style.display = 'none';
    if (adminSection) adminSection.style.display = 'block';
    loadAdminDashboard();
    showToast('Đã vào Bảng Quản Trị Admin Console', 'info');
  } else {
    if (mainContent) mainContent.style.display = 'block';
    if (adminSection) adminSection.style.display = 'none';

    if (sectionId !== 'all') {
      const targetEl = document.getElementById(sectionId);
      if (targetEl) targetEl.scrollIntoView({ behavior: 'smooth' });
    }
  }

  window.scrollTo({ top: 0, behavior: 'smooth' });
}

function switchAdminSubTab(tabName) {
  const tabs = ['pets', 'appointments', 'services', 'products'];
  tabs.forEach(t => {
    const el = document.getElementById(`adminTab${capitalize(t)}`);
    if (el) el.style.display = t === tabName ? 'block' : 'none';
  });

  document.querySelectorAll('.admin-sub-tab').forEach(btn => {
    btn.classList.remove('active', 'btn-primary');
    btn.classList.add('btn-secondary');
  });

  if (event && event.currentTarget) {
    event.currentTarget.classList.remove('btn-secondary');
    event.currentTarget.classList.add('active', 'btn-primary');
  }

  if (tabName === 'pets') loadAdminPetsTable();
  if (tabName === 'appointments') loadAdminAppointmentsTable();
  if (tabName === 'services') loadAdminServicesTable();
  if (tabName === 'products') loadAdminProductsTable();
}

function capitalize(s) {
  return s.charAt(0).toUpperCase() + s.slice(1);
}

/* ==========================================================================
   AUTH MANAGEMENT (JWT + COOKIE + OAUTH2)
   ========================================================================== */
function updateAuthUI() {
  const authNav = document.getElementById('authNavActions');
  if (!authNav) return;

  if (state.currentUser) {
    authNav.innerHTML = `
      <div style="display: flex; align-items: center; gap: 8px; white-space: nowrap; flex-shrink: 0;">
        <img src="${state.currentUser.avatarUrl || 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=200'}" 
             style="width: 32px; height: 32px; border-radius: 50%; object-fit: cover; border: 2px solid var(--primary); flex-shrink: 0;">
        <div style="max-width: 120px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; flex-shrink: 0;">
          <div style="font-weight: 700; font-size: 0.82rem; line-height: 1.2; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;" title="${state.currentUser.fullName}">${state.currentUser.fullName}</div>
          <div style="font-size: 0.7rem; color: var(--primary); font-weight: 600; line-height: 1;">${state.currentUser.role}</div>
        </div>
        <button class="btn btn-secondary btn-sm" onclick="openMyAppointmentsModal()" title="Lịch Sử Đặt Lịch" style="white-space: nowrap; padding: 5px 10px; font-size: 0.8rem;"><i class="far fa-calendar-alt"></i> Lịch Sử</button>
        ${state.currentUser.role === 'Admin' ? '<button class="btn btn-primary btn-sm" onclick="switchTab(\'adminSection\')" style="white-space: nowrap; padding: 5px 10px; font-size: 0.8rem;"><i class="fas fa-chart-line"></i> Quản Trị</button>' : ''}
        <button class="btn btn-secondary btn-sm" onclick="logout()" title="Đăng Xuất" style="white-space: nowrap; padding: 5px 8px; font-size: 0.8rem;"><i class="fas fa-sign-out-alt"></i></button>
      </div>
    `;
  } else {
    authNav.innerHTML = `
      <button class="btn btn-secondary btn-sm" onclick="openModal('loginModal')" style="white-space: nowrap;">Đăng Nhập</button>
      <button class="btn btn-primary btn-sm" onclick="openModal('registerModal')" style="white-space: nowrap;">Đăng Ký</button>
    `;
  }
}



async function handleLogin(e) {
  e.preventDefault();
  const email = document.getElementById('loginEmail').value;
  const password = document.getElementById('loginPassword').value;

  try {
    const res = await fetch(`${API_BASE}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    });

    const data = await res.json();
    if (!res.ok) throw new Error(data.message || 'Đăng nhập thất bại!');

    state.authToken = data.token;
    state.currentUser = data.user;
    localStorage.setItem('authToken', data.token);
    localStorage.setItem('currentUser', JSON.stringify(data.user));
    loadUserCart();

    closeModal('loginModal');

    updateAuthUI();
    loadPets();
    showToast(`Chào mừng trở lại, ${data.user.fullName}!`);

    loadMyAppointments();
    if (data.user.role === 'Admin') loadAdminDashboard();
  } catch (err) {
    showToast(err.message, 'danger');
  }
}

async function handleRegister(e) {
  e.preventDefault();
  const fullName = document.getElementById('regFullName').value;
  const email = document.getElementById('regEmail').value;
  const password = document.getElementById('regPassword').value;
  const phone = document.getElementById('regPhone').value;
  const role = document.getElementById('regRole')?.value || 'Customer';


  try {
    const res = await fetch(`${API_BASE}/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ fullName, email, password, phone, role })
    });

    const data = await res.json();
    if (!res.ok) throw new Error(data.message || 'Đăng ký thất bại!');

    state.authToken = data.token;
    state.currentUser = data.user;
    localStorage.setItem('authToken', data.token);
    localStorage.setItem('currentUser', JSON.stringify(data.user));
    loadUserCart();

    closeModal('registerModal');

    updateAuthUI();
    loadPets();
    showToast('Đăng ký tài khoản thành công!');

  } catch (err) {
    showToast(err.message, 'danger');
  }
}

async function handleOAuth2Login(provider) {
  try {
    const res = await fetch(`${API_BASE}/auth/oauth2-login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        provider: provider,
        email: `user.${provider.toLowerCase()}@example.com`,
        fullName: `Người Dùng ${provider}`,
        avatarUrl: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=200'
      })
    });

    const data = await res.json();
    if (!res.ok) throw new Error(data.message || 'Đăng nhập OAuth2 thất bại');

    state.authToken = data.token;
    state.currentUser = data.user;
    localStorage.setItem('authToken', data.token);
    localStorage.setItem('currentUser', JSON.stringify(data.user));
    loadUserCart();

    closeModal('loginModal');

    updateAuthUI();
    loadPets();
    showToast(`Đã đăng nhập qua ${provider} thành công!`);

  } catch (err) {
    showToast(err.message, 'danger');
  }
}

async function initGoogleOAuth() {
  try {
    const res = await fetch(`${API_BASE}/auth/google-config`);
    if (!res.ok) return;
    const config = await res.json();
    
    const container = document.getElementById('googleBtnContainer');
    const demoBtn = document.getElementById('demoOAuthBtn');

    if (config.isConfigured && typeof google !== 'undefined' && google.accounts && google.accounts.id) {
      google.accounts.id.initialize({
        client_id: config.clientId,
        callback: handleGoogleJwtResponse
      });

      if (container) {
        container.innerHTML = '';
        google.accounts.id.renderButton(container, {
          theme: state.theme === 'dark' ? 'filled_black' : 'outline',
          size: 'large',
          width: 320,
          text: 'signin_with',
          locale: 'vi'
        });
      }
      // Show fallback button as option if official button is blocked by browser extension
      if (demoBtn) demoBtn.style.display = 'block';
    } else {
      if (demoBtn) demoBtn.style.display = 'block';
    }

  } catch (err) {
    console.warn('Google OAuth Init Note:', err);
  }
}

async function handleGoogleJwtResponse(response) {
  if (!response || !response.credential) return;

  try {
    const res = await fetch(`${API_BASE}/auth/google-login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ idToken: response.credential })
    });

    const data = await res.json();
    if (!res.ok) throw new Error(data.message || 'Xác thực Google ID Token thất bại!');

    state.authToken = data.token;
    state.currentUser = data.user;
    localStorage.setItem('authToken', data.token);
    localStorage.setItem('currentUser', JSON.stringify(data.user));
    loadUserCart();

    closeModal('loginModal');

    updateAuthUI();
    loadPets();
    showToast(`Chào mừng, ${data.user.fullName}! Đăng nhập Google thành công.`, 'success');

    loadMyAppointments();
    if (data.user.role === 'Admin') loadAdminDashboard();
  } catch (err) {
    showToast(err.message, 'danger');
  }
}


function logout() {
  fetch(`${API_BASE}/auth/logout`, { method: 'POST' });
  state.currentUser = null;
  state.authToken = null;
  localStorage.removeItem('currentUser');
  localStorage.removeItem('authToken');
  loadUserCart();
  updateAuthUI();
  loadPets();


  switchTab('all');
  showToast('Đã đăng xuất thành công.');
}

/* ==========================================================================
   PET CATALOG (SEARCH, FILTER, SORT, PAGINATION, FULL CRUD)
   ========================================================================== */
async function loadPets() {
  const container = document.getElementById('petGridContainer');
  if (!container) return;

  if (!state.currentUser) {
    container.innerHTML = `
      <div style="grid-column: 1/-1; text-align: center; padding: 60px; background: var(--bg-card); border-radius: var(--radius-lg);">
        <i class="fas fa-paw fa-3x" style="color: var(--primary); margin-bottom: 16px;"></i>
        <h3>Vui lòng đăng nhập để xem danh sách thú cưng của bạn!</h3>
        <p style="color: var(--text-muted); margin-bottom: 16px;">Quản lý hồ sơ, tình trạng sức khỏe và đặt lịch chăm sóc riêng cho thú cưng.</p>
        <button class="btn btn-primary btn-sm" onclick="openModal('loginModal')"><i class="fas fa-sign-in-alt"></i> Đăng Nhập Ngay</button>
      </div>
    `;
    renderPagination('petPagination', 1, 0, () => {});
    return;
  }

  container.innerHTML = '<div style="grid-column: 1/-1; text-align: center; padding: 40px;"><i class="fas fa-spinner fa-spin fa-2x" style="color: var(--primary);"></i><p style="margin-top: 10px;">Đang tải danh sách thú cưng...</p></div>';

  const queryParams = {
    search: state.pets.search,
    species: state.pets.species,
    gender: state.pets.gender,
    sortBy: state.pets.sortBy,
    page: state.pets.page,
    pageSize: state.pets.pageSize
  };

  // Only filter by ownerId if user is Customer (non-Admin)
  // If user is Admin, do NOT filter by ownerId so Admin sees ALL pets across the system
  if (state.currentUser.role !== 'Admin') {
    queryParams.ownerId = state.currentUser.id;
  }

  const params = new URLSearchParams(queryParams);

  try {
    const res = await fetch(`${API_BASE}/pets?${params}`);
    const data = await res.json();

    state.pets.items = data.items;
    state.pets.totalPages = data.totalPages;

    renderPetsGrid(data.items);
    renderPagination('petPagination', data.page, data.totalPages, (page) => {
      state.pets.page = page;
      loadPets();
    });
  } catch (err) {
    container.innerHTML = '<div style="grid-column: 1/-1; text-align: center; color: var(--danger);">Không thể kết nối máy chủ API!</div>';
  }
}

function renderPetsGrid(pets) {
  const container = document.getElementById('petGridContainer');
  if (!pets || pets.length === 0) {
    container.innerHTML = `
      <div style="grid-column: 1/-1; text-align: center; padding: 60px; background: var(--bg-card); border-radius: var(--radius-lg);">
        <i class="fas fa-paw fa-3x" style="color: var(--text-muted); margin-bottom: 16px;"></i>
        <h3>Bạn chưa có hồ sơ thú cưng nào!</h3>
        <p style="color: var(--text-muted); margin-bottom: 16px;">Thêm mới hồ sơ thú cưng của bạn để dễ dàng theo dõi sức khỏe và đặt lịch dịch vụ.</p>
        <button class="btn btn-primary btn-sm" onclick="openPetModal()"><i class="fas fa-plus"></i> Thêm Thú Cưng Mới</button>
      </div>
    `;
    return;
  }

  container.innerHTML = pets.map(pet => `
    <div class="pet-card">
      <div class="pet-card-image">
        <img src="${pet.imageUrl || '/images/poodle_pet_1786347258877.jpg'}" alt="${pet.name}" onerror="this.onerror=null; this.src='/images/poodle_pet_1786347258877.jpg';">
        <span class="pet-badge">${pet.species}</span>
      </div>

      <div class="pet-card-body">
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 4px;">
          <div class="pet-name">${pet.name}</div>
          <span class="badge badge-info" style="font-size: 0.72rem;"><i class="fas fa-user"></i> ${pet.ownerName}</span>
        </div>
        <div class="pet-breed"><i class="fas fa-tag"></i> ${pet.breed}</div>
        <div class="pet-meta">
          <div class="meta-item">
            <label>Giới Tính</label>
            <val>${pet.gender}</val>
          </div>
          <div class="meta-item">
            <label>Tuổi</label>
            <val>${pet.ageYears} Tuổi</val>
          </div>
          <div class="meta-item">
            <label>Cân Nặng</label>
            <val>${pet.weightKg} kg</val>
          </div>
        </div>
        <p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 16px; flex: 1;">${pet.healthNotes || 'Sức khỏe tốt, đã tiêm phòng đầy đủ.'}</p>
        <div class="pet-card-footer">
          <button class="btn btn-primary btn-sm" style="flex: 1;" onclick="openBookingModal(${pet.id}, '${pet.name.replace(/'/g, "\\'")}')">
            <i class="far fa-calendar-check"></i> Đặt Lịch Chăm Sóc
          </button>
          ${(state.currentUser && (state.currentUser.role === 'Admin' || pet.ownerId === state.currentUser.id)) ? `<button class="btn btn-secondary btn-sm" onclick="openPetModal(${pet.id})"><i class="fas fa-edit"></i> Sửa</button>` : ''}
        </div>
      </div>
    </div>
  `).join('');
}


async function openPetModal(id = null) {
  const title = document.getElementById('petModalTitle');
  document.getElementById('editPetId').value = id || '';

  if (id) {
    title.textContent = 'Chỉnh Sửa Hồ Sơ Thú Cưng';
    try {
      const res = await fetch(`${API_BASE}/pets/${id}`);
      const pet = await res.json();
      document.getElementById('addPetName').value = pet.name;
      document.getElementById('addPetSpecies').value = pet.species;
      document.getElementById('addPetBreed').value = pet.breed;
      document.getElementById('addPetAge').value = pet.ageYears;
      document.getElementById('addPetWeight').value = pet.weightKg;
      document.getElementById('addPetGender').value = pet.gender;
      document.getElementById('addPetImage').value = pet.imageUrl || '';
      document.getElementById('addPetNotes').value = pet.healthNotes || '';
    } catch (err) {
      showToast('Không thể tải thông tin thú cưng', 'danger');
    }
  } else {
    title.textContent = 'Thêm Hồ Sơ Thú Cưng Mới';
    document.getElementById('addPetName').value = '';
    document.getElementById('addPetSpecies').value = 'Chó';
    document.getElementById('addPetBreed').value = '';
    document.getElementById('addPetAge').value = '1';
    document.getElementById('addPetWeight').value = '3.5';
    document.getElementById('addPetGender').value = 'Đực';
    document.getElementById('addPetImage').value = '';
    document.getElementById('addPetNotes').value = '';
  }

  openModal('addPetModal');
}

async function handlePetFormSubmit(e) {
  e.preventDefault();
  const id = document.getElementById('editPetId').value;
  const pet = {
    name: document.getElementById('addPetName').value,
    species: document.getElementById('addPetSpecies').value,
    breed: document.getElementById('addPetBreed').value,
    ageYears: parseInt(document.getElementById('addPetAge').value) || 1,
    weightKg: parseFloat(document.getElementById('addPetWeight').value) || 3.5,
    gender: document.getElementById('addPetGender').value,
    imageUrl: document.getElementById('addPetImage').value,
    healthNotes: document.getElementById('addPetNotes').value,
    ownerId: state.currentUser ? state.currentUser.id : 1
  };

  try {
    const url = id ? `${API_BASE}/pets/${id}` : `${API_BASE}/pets`;
    const method = id ? 'PUT' : 'POST';

    const res = await fetch(url, {
      method: method,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(pet)
    });

    if (res.ok) {
      closeModal('addPetModal');
      showToast(id ? 'Đã cập nhật hồ sơ thú cưng!' : 'Đã thêm thú cưng mới!');
      loadPets();
      loadAdminPetsTable();
      loadAdminDashboard();
    }
  } catch (err) {
    showToast('Thao tác thất bại!', 'danger');
  }
}

/* ==========================================================================
   SERVICES & BOOKING
   ========================================================================== */
let globalServices = [];

async function loadServices() {
  const container = document.getElementById('servicesContainer');
  if (!container) return;

  try {
    const res = await fetch(`${API_BASE}/services`);
    globalServices = await res.json();

    container.innerHTML = globalServices.map(srv => `
      <div class="service-card">
        <div class="service-img">
          <img src="${srv.imageUrl || 'https://images.unsplash.com/photo-1516734212186-a967f81ad0d7?w=600'}" alt="${srv.name}">
        </div>
        <span class="badge badge-info" style="width: fit-content; margin-bottom: 8px;">${srv.category}</span>
        <h3 style="font-size: 1.2rem; font-weight: 700; margin-bottom: 6px;">${srv.name}</h3>
        <p style="font-size: 0.9rem; color: var(--text-muted); margin-bottom: 16px; flex: 1;">${srv.description}</p>
        <div style="display: flex; align-items: center; justify-content: space-between; margin-top: auto;">
          <div class="service-price">${Number(srv.price).toLocaleString()} đ</div>
          <button class="btn btn-secondary btn-sm" onclick="openBookingModalWithService(${srv.id})">
            Đặt Ngay <i class="fas fa-arrow-right"></i>
          </button>
        </div>
      </div>
    `).join('');

    populateServiceDropdowns();
  } catch (err) {
    console.error('Failed to load services:', err);
  }
}

function populateServiceDropdowns() {
  const dropdown = document.getElementById('bookingServiceSelect');
  if (!dropdown) return;

  dropdown.innerHTML = '<option value="">-- Chọn Dịch Vụ --</option>' + 
    globalServices.map(s => `<option value="${s.id}">${s.name} - ${Number(s.price).toLocaleString()} đ</option>`).join('');
}

async function openBookingModal(petId, petName) {
  if (!state.currentUser) {
    showToast('Vui lòng đăng nhập để đặt lịch hẹn!', 'warning');
    openModal('loginModal');
    return;
  }

  const petSelect = document.getElementById('bookingPetSelect');
  try {
    const res = await fetch(`${API_BASE}/pets?pageSize=100`);
    const data = await res.json();

    petSelect.innerHTML = data.items.map(p => 
      `<option value="${p.id}" ${p.id === petId ? 'selected' : ''}>${p.name} (${p.breed} - Chủ: ${p.ownerName})</option>`
    ).join('');
  } catch (err) {
    petSelect.innerHTML = '<option value="1">Bé Bông (Poodle)</option><option value="2">Miu Miu (Mèo)</option><option value="3">Mochi (Corgi)</option><option value="4">Loki (Golden)</option>';
  }

  openModal('bookingModal');
}

function openBookingModalWithService(serviceId) {
  const serviceSelect = document.getElementById('bookingServiceSelect');
  if (serviceSelect) serviceSelect.value = serviceId;
  openBookingModal();
}

async function handleBookingSubmit(e) {
  e.preventDefault();
  if (!state.currentUser) {
    showToast('Vui lòng đăng nhập!', 'warning');
    return;
  }

  const petId = parseInt(document.getElementById('bookingPetSelect').value) || 1;
  const serviceId = parseInt(document.getElementById('bookingServiceSelect').value);
  const dateStr = document.getElementById('bookingDate').value;
  const notes = document.getElementById('bookingNotes').value;

  if (!serviceId) {
    showToast('Vui lòng chọn dịch vụ chăm sóc!', 'warning');
    return;
  }

  try {
    const res = await fetch(`${API_BASE}/appointments?customerId=${state.currentUser.id}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        petId: petId,
        serviceId: serviceId,
        appointmentDate: dateStr ? new Date(dateStr).toISOString() : new Date().toISOString(),
        notes: notes
      })
    });

    const data = await res.json();
    if (!res.ok) throw new Error(data.message || 'Đặt lịch thất bại!');

    closeModal('bookingModal');
    showToast('🎉 Đặt lịch hẹn thành công! Đội ngũ sẽ xác nhận sớm.', 'success');
    openMyAppointmentsModal();
    if (state.currentUser.role === 'Admin') loadAdminDashboard();
  } catch (err) {
    showToast(err.message, 'danger');
  }
}


/* ==========================================================================
   PRODUCTS & SHOPPING CART
   ========================================================================== */
async function loadProducts() {
  const container = document.getElementById('productGridContainer');
  if (!container) return;

  const params = new URLSearchParams({
    search: state.products.search,
    category: state.products.category,
    sortBy: state.products.sortBy,
    page: state.products.page,
    pageSize: state.products.pageSize
  });

  try {
    const res = await fetch(`${API_BASE}/products?${params}`);
    const data = await res.json();

    state.products.items = data.items;
    state.products.totalPages = data.totalPages;

    renderProductsGrid(data.items);
    renderPagination('productPagination', data.page, data.totalPages, (page) => {
      state.products.page = page;
      loadProducts();
    });
  } catch (err) {
    console.error(err);
  }
}

function renderProductsGrid(products) {
  const container = document.getElementById('productGridContainer');
  if (!products || products.length === 0) {
    container.innerHTML = '<div style="grid-column: 1/-1; text-align: center; padding: 40px;">Không có sản phẩm nào.</div>';
    return;
  }

  container.innerHTML = products.map(p => `
    <div class="product-card">
      <div class="product-img">
        <img src="${p.imageUrl || '/images/poodle_pet_1786347258877.jpg'}" alt="${p.name}" onerror="this.onerror=null; this.src='/images/poodle_pet_1786347258877.jpg';">
      </div>

      <span class="badge badge-warning" style="width: fit-content; margin-bottom: 6px;">${p.category}</span>
      <div class="product-title">${p.name}</div>
      <div style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 10px;">⭐ ${p.rating} | Còn: ${p.stockQuantity}</div>
      <div style="display: flex; align-items: center; justify-content: space-between; margin-top: auto;">
        <div class="product-price">${Number(p.price).toLocaleString()} đ</div>
        <button class="btn btn-primary btn-sm" onclick="addToCart(${p.id}, '${p.name.replace(/'/g, "\\'")}', ${p.price}, '${p.imageUrl}')">
          <i class="fas fa-cart-plus"></i> Thêm
        </button>
      </div>
    </div>
  `).join('');
}

function getCartStorageKey() {
  if (state.currentUser && state.currentUser.id) {
    return `petCart_user_${state.currentUser.id}`;
  }
  return 'petCart_guest';
}

function loadUserCart() {
  const key = getCartStorageKey();
  state.cart = JSON.parse(localStorage.getItem(key)) || [];
  updateCartBadge();
}

function saveUserCart() {
  const key = getCartStorageKey();
  localStorage.setItem(key, JSON.stringify(state.cart));
  updateCartBadge();
}

function addToCart(id, name, price, imageUrl) {
  const existing = state.cart.find(item => item.id === id);
  if (existing) {
    existing.quantity += 1;
  } else {
    state.cart.push({ id, name, price, imageUrl, quantity: 1 });
  }
  saveUserCart();
  showToast(`Đã thêm "${name}" vào giỏ hàng!`, 'success');
}

function updateCartBadge() {
  const count = state.cart.reduce((sum, item) => sum + item.quantity, 0);
  const badge = document.getElementById('cartBadgeCount');
  if (badge) badge.textContent = count;
}

function openCartModal() {
  renderCartItems();
  openModal('cartModal');
}

function renderCartItems() {
  const container = document.getElementById('cartItemsList');
  const totalPriceEl = document.getElementById('cartTotalPrice');
  if (!container) return;

  if (!state.cart || state.cart.length === 0) {
    container.innerHTML = `
      <div style="text-align: center; padding: 40px 20px;">
        <i class="fas fa-shopping-bag fa-3x" style="color: var(--text-muted); margin-bottom: 16px;"></i>
        <h4 style="margin-bottom: 8px;">Giỏ hàng của bạn đang trống!</h4>
        <p style="color: var(--text-muted); font-size: 0.9rem;">Hãy dạo cửa hàng và chọn những sản phẩm ưng ý cho thú cưng nhé.</p>
      </div>
    `;
    if (totalPriceEl) totalPriceEl.textContent = '0 đ';
    return;
  }

  let total = 0;
  container.innerHTML = state.cart.map(item => {
    const itemSubtotal = item.price * item.quantity;
    total += itemSubtotal;

    return `
      <div style="display: flex; align-items: center; justify-content: space-between; padding: 12px 0; border-bottom: 1px solid var(--border-glass); gap: 12px;">
        <img src="${item.imageUrl || 'https://images.unsplash.com/photo-1589924691995-400dc9ecc119?w=200'}" 
             alt="${item.name}" style="width: 54px; height: 54px; border-radius: var(--radius-md); object-fit: cover;">
        
        <div style="flex: 1;">
          <div style="font-weight: 700; font-size: 0.95rem; line-height: 1.3;">${item.name}</div>
          <div style="font-size: 0.85rem; color: var(--primary); font-weight: 600; margin-top: 2px;">
            ${Number(item.price).toLocaleString()} đ
          </div>
        </div>

        <div style="display: flex; align-items: center; gap: 8px; background: var(--bg-card); padding: 4px 8px; border-radius: var(--radius-md); border: 1px solid var(--border-glass);">
          <button class="btn btn-secondary btn-sm" style="padding: 2px 8px; height: 26px; min-width: 26px;" onclick="updateCartQuantity(${item.id}, -1)">-</button>
          <span style="font-weight: 700; min-width: 20px; text-align: center; font-size: 0.9rem;">${item.quantity}</span>
          <button class="btn btn-secondary btn-sm" style="padding: 2px 8px; height: 26px; min-width: 26px;" onclick="updateCartQuantity(${item.id}, 1)">+</button>
        </div>

        <div style="font-weight: 800; font-size: 0.95rem; text-align: right; min-width: 85px; color: var(--text-main);">
          ${Number(itemSubtotal).toLocaleString()} đ
        </div>

        <button class="btn btn-secondary btn-sm" style="color: var(--danger); padding: 6px 8px;" onclick="removeFromCart(${item.id})" title="Xóa khỏi giỏ hàng">
          <i class="fas fa-trash-alt"></i>
        </button>
      </div>
    `;
  }).join('');

  if (totalPriceEl) totalPriceEl.textContent = `${Number(total).toLocaleString()} đ`;
}

function updateCartQuantity(id, delta) {
  const item = state.cart.find(i => i.id === id);
  if (!item) return;

  item.quantity += delta;
  if (item.quantity <= 0) {
    state.cart = state.cart.filter(i => i.id !== id);
  }

  saveUserCart();
  renderCartItems();
}

function removeFromCart(id) {
  state.cart = state.cart.filter(i => i.id !== id);
  saveUserCart();
  renderCartItems();
  showToast('Đã xóa sản phẩm khỏi giỏ hàng', 'info');
}

function clearCart() {
  if (state.cart.length === 0) return;
  state.cart = [];
  saveUserCart();
  renderCartItems();
  showToast('Đã xóa sạch giỏ hàng!', 'info');
}


function openCheckoutModal() {
  if (!state.cart || state.cart.length === 0) {
    showToast('Giỏ hàng của bạn đang trống!', 'warning');
    return;
  }

  const total = state.cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
  const checkoutTotalEl = document.getElementById('checkoutTotalAmount');
  if (checkoutTotalEl) checkoutTotalEl.textContent = `${Number(total).toLocaleString()} đ`;

  if (state.currentUser) {
    const nameInput = document.getElementById('checkoutName');
    const phoneInput = document.getElementById('checkoutPhone');
    const addressInput = document.getElementById('checkoutAddress');

    if (nameInput && !nameInput.value) nameInput.value = state.currentUser.fullName || '';
    if (phoneInput && !phoneInput.value) phoneInput.value = state.currentUser.phone || '';
    if (addressInput && !addressInput.value) addressInput.value = state.currentUser.address || '';
  }

  closeModal('cartModal');
  openModal('checkoutModal');
}

async function handleCheckoutSubmit(e) {
  e.preventDefault();
  const name = document.getElementById('checkoutName').value;
  const phone = document.getElementById('checkoutPhone').value;
  const address = document.getElementById('checkoutAddress').value;
  const paymentMethod = document.getElementById('checkoutPaymentMethod').value;

  if (state.cart.length === 0) {
    showToast('Giỏ hàng của bạn đang trống!', 'warning');
    return;
  }

  const items = state.cart.map(item => ({
    id: item.id,
    quantity: item.quantity
  }));

  try {
    const res = await fetch(`${API_BASE}/products/checkout`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        customerName: name,
        customerPhone: phone,
        shippingAddress: address,
        paymentMethod: paymentMethod,
        items: items
      })
    });

    const data = await res.json();
    if (!res.ok) throw new Error(data.message || 'Thanh toán thất bại!');

    clearCart();
    closeModal('checkoutModal');

    showToast(`🎉 Đặt hàng thành công! Đơn hàng ${Number(data.totalAmount).toLocaleString()} đ đang được giao tới ${name}.`, 'success');

    loadProducts();
    if (state.currentUser && state.currentUser.role === 'Admin') {
      loadAdminProductsTable();
      loadAdminDashboard();
    }
  } catch (err) {
    showToast(err.message, 'danger');
  }
}



/* ==========================================================================
   MY APPOINTMENTS
   ========================================================================== */
function openMyAppointmentsModal() {
  if (!state.currentUser) {
    showToast('Vui lòng đăng nhập để xem lịch sử đặt lịch!', 'warning');
    openModal('loginModal');
    return;
  }
  loadMyAppointments();
  openModal('myAppointmentsModal');
}

async function cancelAppointment(id) {
  if (!confirm('Bạn có chắc chắn muốn hủy lịch hẹn này?')) return;
  try {
    const res = await fetch(`${API_BASE}/appointments/${id}`, { method: 'DELETE' });
    if (res.ok) {
      showToast('Đã hủy lịch hẹn thành công!', 'info');
      loadMyAppointments();
      if (state.currentUser && state.currentUser.role === 'Admin') {
        loadAdminAppointmentsTable();
        loadAdminDashboard();
      }
    }
  } catch (err) {
    showToast('Thao tác hủy lịch thất bại', 'danger');
  }
}

async function loadMyAppointments() {
  const container = document.getElementById('myAppointmentsList');
  if (!container || !state.currentUser) return;

  try {
    const res = await fetch(`${API_BASE}/appointments?customerId=${state.currentUser.id}`);
    const items = await res.json();

    if (items.length === 0) {
      container.innerHTML = `
        <div style="text-align: center; padding: 40px 20px;">
          <i class="far fa-calendar-times fa-3x" style="color: var(--text-muted); margin-bottom: 16px;"></i>
          <h4>Bạn chưa có lịch hẹn dịch vụ nào!</h4>
          <p style="color: var(--text-muted); font-size: 0.9rem;">Hãy chọn gói dịch vụ spa hoặc khám bệnh thích hợp để chăm sóc cho bé yêu.</p>
        </div>
      `;
      return;
    }

    container.innerHTML = items.map(a => `
      <div style="background: var(--bg-card); border: 1px solid var(--border-glass); border-radius: var(--radius-md); padding: 16px; margin-bottom: 12px; display: flex; align-items: center; justify-content: space-between; gap: 16px; flex-wrap: wrap;">
        <div>
          <div style="font-weight: 800; font-size: 1.1rem; color: var(--primary);">${a.serviceName}</div>
          <div style="font-size: 0.9rem; margin-top: 2px;">Thú cưng: <strong>${a.petName}</strong> (${a.petSpecies})</div>
          <div style="font-size: 0.85rem; color: var(--text-muted); margin-top: 4px;"><i class="far fa-clock"></i> ${new Date(a.appointmentDate).toLocaleString('vi-VN')}</div>
          ${a.notes ? `<div style="font-size: 0.82rem; color: var(--text-muted); margin-top: 4px;"><i>Ghi chú: ${a.notes}</i></div>` : ''}
        </div>
        <div style="text-align: right; display: flex; flex-direction: column; align-items: flex-end; gap: 6px;">
          <span class="badge ${getStatusBadgeClass(a.status)}">${getFriendlyStatusText(a.status)}</span>
          <div style="font-weight: 800; font-size: 1.05rem; color: var(--primary);">${Number(a.totalPrice).toLocaleString()} đ</div>
          ${(a.status === 'Pending' || a.status === 'Confirmed') ? `
            <button class="btn btn-secondary btn-sm" style="color: var(--danger); border-color: var(--danger); padding: 2px 10px; font-size: 0.78rem;" onclick="cancelAppointment(${a.id})">
              <i class="fas fa-times"></i> Hủy Lịch
            </button>
          ` : ''}
        </div>
      </div>
    `).join('');
  } catch (err) {
    console.error(err);
  }
}

function getFriendlyStatusText(status) {
  switch (status) {
    case 'Pending': return 'Chờ Xác Nhận';
    case 'Confirmed': return 'Đã Xác Nhận';
    case 'Completed': return 'Đã Hoàn Thành';
    case 'Cancelled': return 'Đã Hủy';
    default: return status;
  }
}

function getStatusBadgeClass(status) {
  switch (status) {
    case 'Confirmed': return 'badge-info';
    case 'Completed': return 'badge-success';
    case 'Cancelled': return 'badge-danger';
    default: return 'badge-warning';
  }
}


/* ==========================================================================
   ADMIN DASHBOARD & FULL CRUD MANAGEMENT
   ========================================================================== */
async function loadAdminDashboard() {
  try {
    const res = await fetch(`${API_BASE}/dashboard/stats`);
    const stats = await res.json();

    document.getElementById('statTotalPets').textContent = stats.totalPets;
    document.getElementById('statTotalAppointments').textContent = stats.totalAppointments;
    document.getElementById('statPendingAppointments').textContent = stats.pendingAppointments;
    document.getElementById('statTotalRevenue').textContent = Number(stats.totalRevenue).toLocaleString() + ' đ';

    loadAdminPetsTable();
  } catch (err) {
    console.error(err);
  }
}

// PETS CRUD
async function loadAdminPetsTable() {
  const tableBody = document.getElementById('adminTableBody');
  if (!tableBody) return;

  try {
    const res = await fetch(`${API_BASE}/pets?pageSize=50`);
    const data = await res.json();

    tableBody.innerHTML = data.items.map(p => `
      <tr>
        <td>#${p.id}</td>
        <td>
          <div style="display: flex; align-items: center; gap: 10px;">
            <img src="${p.imageUrl}" style="width: 36px; height: 36px; border-radius: 50%; object-fit: cover;" onerror="this.onerror=null; this.src='/images/poodle_pet_1786347258877.jpg';">
            <strong>${p.name}</strong>
          </div>
        </td>

        <td>${p.species} / ${p.breed}</td>
        <td>${p.ageYears} Tuổi (${p.weightKg}kg)</td>
        <td><span class="badge badge-info"><i class="fas fa-user"></i> ${p.ownerName}</span></td>
        <td>
          <button class="btn btn-secondary btn-sm" onclick="openPetModal(${p.id})"><i class="fas fa-edit"></i> Sửa</button>
          <button class="btn btn-secondary btn-sm" onclick="deletePet(${p.id})"><i class="fas fa-trash" style="color: var(--danger);"></i> Xóa</button>
        </td>
      </tr>
    `).join('');
  } catch (err) {
    console.error(err);
  }
}

async function deletePet(id) {
  if (!confirm('Bạn có chắc chắn muốn xóa thú cưng này?')) return;
  try {
    const res = await fetch(`${API_BASE}/pets/${id}`, { method: 'DELETE' });
    if (res.ok) {
      showToast('Đã xóa thú cưng thành công!');
      loadAdminPetsTable();
      loadPets();
      loadAdminDashboard();
    }
  } catch (err) {
    showToast('Xóa thất bại', 'danger');
  }
}

// APPOINTMENTS CRUD
async function loadAdminAppointmentsTable() {
  const tableBody = document.getElementById('adminAppointmentsBody');
  if (!tableBody) return;

  try {
    const res = await fetch(`${API_BASE}/appointments`);
    const items = await res.json();

    tableBody.innerHTML = items.map(a => `
      <tr>
        <td>#${a.id}</td>
        <td>${a.customerName} (${a.customerPhone})</td>
        <td>${a.petName} (${a.petSpecies})</td>
        <td>${a.serviceName}</td>
        <td>${new Date(a.appointmentDate).toLocaleString('vi-VN')}</td>
        <td><span class="badge ${getStatusBadgeClass(a.status)}">${a.status}</span></td>
        <td>
          ${a.status === 'Pending' ? `<button class="btn btn-primary btn-sm" onclick="updateAppointmentStatus(${a.id}, 'Confirmed')">Duyệt</button>` : ''}
          ${a.status === 'Confirmed' ? `<button class="btn btn-secondary btn-sm" onclick="updateAppointmentStatus(${a.id}, 'Completed')">Hoàn Thành</button>` : ''}
          ${a.status !== 'Cancelled' && a.status !== 'Completed' ? `<button class="btn btn-danger btn-sm" style="margin-left:4px;" onclick="updateAppointmentStatus(${a.id}, 'Cancelled')">Hủy</button>` : ''}
        </td>
      </tr>
    `).join('');
  } catch (err) {
    console.error(err);
  }
}

async function updateAppointmentStatus(id, status) {
  try {
    const res = await fetch(`${API_BASE}/appointments/${id}/status`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(status)
    });

    if (res.ok) {
      showToast(`Đã đổi trạng thái lịch hẹn #${id} thành ${status}!`);
      loadAdminAppointmentsTable();
      loadAdminDashboard();
    }
  } catch (err) {
    showToast('Cập nhật thất bại!', 'danger');
  }
}

// SERVICES CRUD
async function loadAdminServicesTable() {
  const tableBody = document.getElementById('adminServicesBody');
  if (!tableBody) return;

  try {
    const res = await fetch(`${API_BASE}/services`);
    const services = await res.json();

    tableBody.innerHTML = services.map(s => `
      <tr>
        <td>#${s.id}</td>
        <td><strong>${s.name}</strong></td>
        <td>${s.category}</td>
        <td>${s.durationMinutes} phút</td>
        <td>${Number(s.price).toLocaleString()} đ</td>
        <td><span class="badge badge-success">${s.isActive ? 'Hoạt Động' : 'Tạm Dừng'}</span></td>
        <td>
          <button class="btn btn-secondary btn-sm" onclick="openServiceModal(${s.id})"><i class="fas fa-edit"></i> Sửa</button>
          <button class="btn btn-secondary btn-sm" onclick="deleteService(${s.id})"><i class="fas fa-trash" style="color: var(--danger);"></i> Xóa</button>
        </td>
      </tr>
    `).join('');
  } catch (err) {
    console.error(err);
  }
}

async function openServiceModal(id = null) {
  const title = document.getElementById('serviceModalTitle');
  document.getElementById('srvId').value = id || '';

  if (id) {
    title.textContent = 'Chỉnh Sửa Dịch Vụ';
    try {
      const res = await fetch(`${API_BASE}/services/${id}`);
      const srv = await res.json();
      document.getElementById('srvName').value = srv.name;
      document.getElementById('srvCategory').value = srv.category;
      document.getElementById('srvPrice').value = srv.price;
      document.getElementById('srvDuration').value = srv.durationMinutes;
      document.getElementById('srvImage').value = srv.imageUrl;
      document.getElementById('srvDesc').value = srv.description;
    } catch (err) {
      showToast('Không thể tải dịch vụ', 'danger');
    }
  } else {
    title.textContent = 'Thêm Dịch Vụ Mới';
    document.getElementById('srvName').value = '';
    document.getElementById('srvPrice').value = '250000';
    document.getElementById('srvDuration').value = '45';
    document.getElementById('srvImage').value = '';
    document.getElementById('srvDesc').value = '';
  }

  openModal('serviceModal');
}

async function handleServiceFormSubmit(e) {
  e.preventDefault();
  const id = document.getElementById('srvId').value;
  const srv = {
    name: document.getElementById('srvName').value,
    category: document.getElementById('srvCategory').value,
    price: parseFloat(document.getElementById('srvPrice').value) || 0,
    durationMinutes: parseInt(document.getElementById('srvDuration').value) || 30,
    imageUrl: document.getElementById('srvImage').value || 'https://images.unsplash.com/photo-1516734212186-a967f81ad0d7?w=600',
    description: document.getElementById('srvDesc').value,
    isActive: true
  };

  try {
    const url = id ? `${API_BASE}/services/${id}` : `${API_BASE}/services`;
    const method = id ? 'PUT' : 'POST';

    const res = await fetch(url, {
      method: method,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(srv)
    });

    if (res.ok) {
      closeModal('serviceModal');
      showToast(id ? 'Đã cập nhật dịch vụ!' : 'Đã thêm dịch vụ mới!');
      loadAdminServicesTable();
      loadServices();
    }
  } catch (err) {
    showToast('Thao tác thất bại!', 'danger');
  }
}

async function deleteService(id) {
  if (!confirm('Bạn có chắc chắn muốn ngưng cung cấp dịch vụ này?')) return;
  try {
    const res = await fetch(`${API_BASE}/services/${id}`, { method: 'DELETE' });
    if (res.ok) {
      showToast('Đã xóa dịch vụ thành công!');
      loadAdminServicesTable();
      loadServices();
    }
  } catch (err) {
    showToast('Xóa dịch vụ thất bại', 'danger');
  }
}

// PRODUCTS CRUD
async function loadAdminProductsTable() {
  const tableBody = document.getElementById('adminProductsBody');
  if (!tableBody) return;

  try {
    const res = await fetch(`${API_BASE}/products?pageSize=50`);
    const data = await res.json();

    tableBody.innerHTML = data.items.map(p => `
      <tr>
        <td>#${p.id}</td>
        <td>
          <div style="display: flex; align-items: center; gap: 10px;">
            <img src="${p.imageUrl}" style="width: 36px; height: 36px; border-radius: 8px; object-fit: cover;" onerror="this.onerror=null; this.src='/images/poodle_pet_1786347258877.jpg';">
            <strong>${p.name}</strong>
          </div>
        </td>

        <td>${p.category}</td>
        <td>${p.stockQuantity} món</td>
        <td>${Number(p.price).toLocaleString()} đ</td>
        <td>⭐ ${p.rating}</td>
        <td>
          <button class="btn btn-secondary btn-sm" onclick="openProductModal(${p.id})"><i class="fas fa-edit"></i> Sửa</button>
          <button class="btn btn-secondary btn-sm" onclick="deleteProduct(${p.id})"><i class="fas fa-trash" style="color: var(--danger);"></i> Xóa</button>
        </td>
      </tr>
    `).join('');
  } catch (err) {
    console.error(err);
  }
}

async function openProductModal(id = null) {
  const title = document.getElementById('productModalTitle');
  document.getElementById('prodId').value = id || '';

  if (id) {
    title.textContent = 'Chỉnh Sửa Sản Phẩm';
    try {
      const res = await fetch(`${API_BASE}/products/${id}`);
      const prod = await res.json();
      document.getElementById('prodName').value = prod.name;
      document.getElementById('prodCategory').value = prod.category;
      document.getElementById('prodPrice').value = prod.price;
      document.getElementById('prodStock').value = prod.stockQuantity;
      document.getElementById('prodRating').value = prod.rating;
      document.getElementById('prodImage').value = prod.imageUrl;
      document.getElementById('prodDesc').value = prod.description;
    } catch (err) {
      showToast('Không thể tải thông tin sản phẩm', 'danger');
    }
  } else {
    title.textContent = 'Thêm Sản Phẩm Mới';
    document.getElementById('prodName').value = '';
    document.getElementById('prodPrice').value = '150000';
    document.getElementById('prodStock').value = '50';
    document.getElementById('prodRating').value = '4.8';
    document.getElementById('prodImage').value = '';
    document.getElementById('prodDesc').value = '';
  }

  openModal('productModal');
}

async function handleProductFormSubmit(e) {
  e.preventDefault();
  const id = document.getElementById('prodId').value;
  const prod = {
    name: document.getElementById('prodName').value,
    category: document.getElementById('prodCategory').value,
    price: parseFloat(document.getElementById('prodPrice').value) || 0,
    stockQuantity: parseInt(document.getElementById('prodStock').value) || 0,
    rating: parseFloat(document.getElementById('prodRating').value) || 4.8,
    imageUrl: document.getElementById('prodImage').value || 'https://images.unsplash.com/photo-1589924691995-400dc9ecc119?w=600',
    description: document.getElementById('prodDesc').value
  };

  try {
    const url = id ? `${API_BASE}/products/${id}` : `${API_BASE}/products`;
    const method = id ? 'PUT' : 'POST';

    const res = await fetch(url, {
      method: method,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(prod)
    });

    if (res.ok) {
      closeModal('productModal');
      showToast(id ? 'Đã cập nhật sản phẩm thành công!' : 'Đã thêm sản phẩm mới thành công!');
      loadAdminProductsTable();
      loadProducts();
      loadAdminDashboard();
    }
  } catch (err) {
    showToast('Thao tác thất bại!', 'danger');
  }
}

async function deleteProduct(id) {
  if (!confirm('Bạn có chắc chắn muốn xóa sản phẩm này?')) return;
  try {
    const res = await fetch(`${API_BASE}/products/${id}`, { method: 'DELETE' });
    if (res.ok) {
      showToast('Đã xóa sản phẩm thành công!');
      loadAdminProductsTable();
      loadProducts();
      loadAdminDashboard();
    }
  } catch (err) {
    showToast('Xóa sản phẩm thất bại', 'danger');
  }
}

/* ==========================================================================
   UI UTILITIES (PAGINATION, MODALS, TOASTS)
   ========================================================================== */
function renderPagination(containerId, page, totalPages, onPageChange) {
  const container = document.getElementById(containerId);
  if (!container || totalPages <= 1) {
    if (container) container.innerHTML = '';
    return;
  }

  let html = '';
  for (let i = 1; i <= totalPages; i++) {
    html += `<button class="page-btn ${i === page ? 'active' : ''}" onclick="onPageClick('${containerId}', ${i})">${i}</button>`;
  }
  container.innerHTML = html;
  window[`_onPage_${containerId}`] = onPageChange;
}

function onPageClick(containerId, page) {
  if (window[`_onPage_${containerId}`]) {
    window[`_onPage_${containerId}`](page);
  }
}

function openModal(id) {
  const modal = document.getElementById(id);
  if (modal) modal.classList.add('active');
  if (id === 'loginModal') {
    setTimeout(initGoogleOAuth, 100);
  }
}


function closeModal(id) {
  const modal = document.getElementById(id);
  if (modal) modal.classList.remove('active');
}

function showToast(message, type = 'success') {
  const container = document.getElementById('toastContainer');
  if (!container) return;

  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.innerHTML = `
    <i class="fas ${type === 'success' ? 'fa-check-circle' : 'fa-exclamation-circle'}" style="color: ${type === 'success' ? 'var(--primary)' : 'var(--danger)'};"></i>
    <span>${message}</span>
  `;

  container.appendChild(toast);
  setTimeout(() => {
    toast.remove();
  }, 4000);
}

function setupEventListeners() {
  document.getElementById('themeToggle')?.addEventListener('click', toggleTheme);

  // Close modals on clicking overlay backdrop
  document.querySelectorAll('.modal-overlay').forEach(overlay => {
    overlay.addEventListener('click', (e) => {
      if (e.target === overlay) {
        overlay.classList.remove('active');
      }
    });
  });

  // Close modals on ESC key
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      document.querySelectorAll('.modal-overlay.active').forEach(modal => {
        modal.classList.remove('active');
      });
    }
  });

  document.getElementById('petSearchInput')?.addEventListener('input', (e) => {
    state.pets.search = e.target.value;
    state.pets.page = 1;
    loadPets();
  });


  document.getElementById('petSpeciesFilter')?.addEventListener('change', (e) => {
    state.pets.species = e.target.value;
    state.pets.page = 1;
    loadPets();
  });

  document.getElementById('petSortSelect')?.addEventListener('change', (e) => {
    state.pets.sortBy = e.target.value;
    loadPets();
  });

  document.getElementById('productSearchInput')?.addEventListener('input', (e) => {
    state.products.search = e.target.value;
    state.products.page = 1;
    loadProducts();
  });

  document.getElementById('productCategoryFilter')?.addEventListener('change', (e) => {
    state.products.category = e.target.value;
    state.products.page = 1;
    loadProducts();
  });
}
