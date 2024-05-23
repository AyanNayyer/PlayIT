
export default {
    template: 
    `<div class="container" style="margin-top: 20px; align-items: center; display: flex; flex-direction: column; font-family:'Times New Roman', Times, serif">
        <h1><u>ADMIN Login</u></h1>
        <div class="mb-3 p-5 bg-light" style="margin-top: 10px">
            <label for="user_email" class="form-label">Email address</label>
            <input type="email" class="form-control" id="user_email" placeholder="name@example.com" v-model="login_details.email">
            <label for="user_password" class="form-label">Password</label>
            <input type="password" class="form-control" id="user_password" v-model="login_details.password">
            <br>
            <div class="text-center">
            <button type="submit" class="btn btn-primary" @click="login">Login</button>
            </div>
            <br>
            <h6> 
                <button type="button" class="btn btn-link" @click="user_login"> User Login</button>
            </h6>
        </div>
        <img src="/static/playit.png" alt="playit Logo" style="margin-top: 20px; max-width: 150px;">
  </div>
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
            const response = await fetch('/admin_login', {
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
            }
            else {
                const error = await response.json();
                alert(error.message);
            }
        },
        user_login(){
            this.$router.push('/login')
        }
    },
}