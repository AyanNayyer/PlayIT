export default {
    template:
    `<div class="container" style="margin-top: 20px; align-items: center; display: flex; flex-direction: column; font-family:'Times New Roman', Times, serif">
        <h1><u>Register</u></h1>
        <div class="mb-3 p-5 bg-light" style="margin-top: 10px">
            <label for="user_username" class="form-label">Username</label>
            <input type="username" class="form-control" id="user_username" placeholder="username" v-model="register_details.username">
            <label for="user_email" class="form-label">Email address</label>
            <input type="email" class="form-control" id="user_email" placeholder="name@example.com" v-model="register_details.email">
            <label for="user_password" class="form-label">Password</label>
            <input type="password" class="form-control" id="user_password" v-model="register_details.password">
            <br>
            <div class="text-center">
            <button type="button" class="btn btn-primary" @click="register">Register</button>
            </div>
            <br>
            <h6> 
                Already Registered?  <button type="button" class="btn btn-link" @click="login">Login</button>
            </h6>
        </div>
        <img src="/static/playit.png" alt="playit Logo" style="margin-top: 20px; max-width: 150px;">
  </div>
    </div>`,
    data() {
        return {
            register_details: {
                email: null,
                username: null,
                password: null
            },
        }
    },
    methods: {
        async register() {
            if (!this.isValidEmail(this.register_details.email)){
                alert("Invalid email address")
                return
            }
            else{
                const response = await fetch('/user_register', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(this.register_details)
                })
                if (response.status == 200) {
                    const response_data = await response.json();
                    alert(response_data.message);
                    this.$router.push('/user_login')
                }
                else {
                    const error = await response.json();
                    alert(error.message);
                }

            }
            
        },

        login(){
            this.$router.push('/user_login')
        },

        isValidEmail(email) {
            // Regular expression for basic email validation
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            return emailRegex.test(email);
        },
    },

}