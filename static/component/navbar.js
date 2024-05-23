export default {
    template: `
      <nav class="navbar navbar-expand-lg navbar-light" style="background-color: #8ae68a;">
          <div class="container-fluid">
              <router-link :to="is_logged_in ? (is_admin ? '/admin_dash' : '/user_dash') : '/'" class="navbar-brand">
                  <img src="/static/playit.png" alt="PlayIT Logo" height="30" class="d-inline-block align-top">
              </router-link>
              <ul class="navbar-nav ms-auto my-2 my-lg-0 navbar-nav-scroll" style="--bs-scroll-height: 100px;">
                  <li class="nav-item" v-if="!is_logged_in">
                      <button class="nav-link" @click='admin_login'>Admin Login</button>
                  </li>
              </ul>
  
              <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarScroll" aria-controls="navbarScroll" aria-expanded="false" aria-label="Toggle navigation">
                  <span class="navbar-toggler-icon"></span>
              </button>
  
              <div class="collapse navbar-collapse" id="navbarScroll" v-if="is_logged_in">
                  <ul class="navbar-nav me-auto my-2 my-lg-0 navbar-nav-scroll" style="--bs-scroll-height: 100px; ">
                      <li class="nav-item">
                          <button class="nav-link" @click='dashboard'>Dashboard</button>
                      </li>
                      <li class="nav-item" v-if="this.role.includes('user')">
                          <button class="nav-link" @click='artist_account'>Artist Account</button>
                      </li>
                  </ul>
                  <ul class="navbar-nav ms-auto my-2 my-lg-0 navbar-nav-scroll" style="--bs-scroll-height: 100px;">
                      <li class="nav-item">
                          <button class="nav-link" @click='logout'>Logout</button>
                      </li>
                  </ul>    
              </div>
          </div>
      </nav>
      `,
      data() {
          return{
              role: localStorage.getItem('role'),
              token: localStorage.getItem('auth_token'),
          }
      },
      computed: {
          is_logged_in() {
              return localStorage.getItem('auth_token') !== null;
          },
          is_admin() {
              return this.role.includes('admin');
          }
      },
      methods: {
          logout() {
              localStorage.removeItem('auth_token');
              localStorage.removeItem('role');
              localStorage.removeItem('songs');
              this.$router.push('/');
          },
          dashboard() {
              if (this.is_admin) {
                  this.$router.push('/admin_dash')
              } else if (this.role.includes('user')) {
                  this.$router.push('/user_dash')
              } else {
                  console.log('role not found')
              }
          },
          artist_account() {
              if (this.role.includes('user')) {
                  this.$router.push('/artist_dash')
              }
          },
          admin_login(){
              this.$router.push('/admin_login')
          },
      }
  }
  