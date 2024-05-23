export default {
    template: 
    `<div class="container" style="margin-top: 20px; align-items: center; display: flex; flex-direction: column; font-family: 'Times New Roman', Times, serif">
    <h1 class="mb-4"><u>Login</u></h1>
    <div class="mb-3 p-5 bg-light rounded" style="margin-top: 10px; width: 300px;">
      <label for="user_email" class="form-label">Email address</label>
      <input type="email" class="form-control" id="user_email" placeholder="name@example.com" v-model="login_details.email">
      <label for="user_password" class="form-label mt-3">Password</label>
      <input type="password" class="form-control" id="user_password" v-model="login_details.password">
      <div class="text-center mt-4">
        <button type="button" class="btn btn-primary" @click="login">Login</button>
      </div>
      <div class="text-center mt-3">
        <h6> 
          New User? <router-link to="/user_register" class="btn btn-link">Register</router-link>
        </h6>
      </div>
    </div>
   <img src="/static/playit.png" alt="playit Logo" style="margin-top: 20px; max-width: 150px;">
  </div>`,
    data() {
        return {
            login_details: {
                email: null,
                password: null
            },
        }
    },
    methods: {
        async login() {
            if (!this.isValidEmail(this.login_details.email)){
                alert("Invalid email address")
                return
            }
            else{
                const response = await fetch('/user_login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(this.login_details)
                })
                
                if (response.status == 200) {
                    const response_data = await response.json();
                    // console.log(response_data)
                    localStorage.setItem('auth_token', response_data.auth_token);
                    localStorage.setItem('role', response_data.role);

                    // to check list element in javascript:- list.includes('element')
                    if (response_data.role.includes('admin')) {
                        this.$router.push('/admin_dash')
                    }
                    if (response_data.role.includes('user')) {
                        this.$router.push('/user_dash');
                    }
                }
                else {
                    const error = await response.json();
                    alert(error.message);
                }

            }
            
        },
        register(){
            this.$router.push('/user_register')
        },

        isValidEmail(email) {
            // Regular expression for basic email validation
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            return emailRegex.test(email);
        },
    },
}