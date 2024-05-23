
export default {
    template: `
    <div>
        <div style="background-image: url('/static/playit.png'); background-size: contain; background-position: center center; background-repeat: no-repeat; height: 25vh; display: flex; flex-direction: column; justify-content: center; align-items: center;">
        </div>
        <div class="container text-center my-5" >
        <h1 class="display-4">Welcome to <b><u><span style="color: lightgreen;">PlayIT</span></u></b> - Music for <b>ALL</b></h1>
        <p class="lead">Click on the buttons below to get started.</p>
        </div>
  
        <div class="container text-center">
          <button @click="login" class="btn btn-primary btn-lg mx-2">Login</button>
          <button @click="register" class="btn btn-secondary btn-lg mx-2">Register</button>
        </div>
    </div>
    `,
    data() {
      return {
        message: 'Welcome to the Home Page',
      };
    },
    methods: {
      login() {
        this.$router.push('/user_login');
      },
      register() {
        this.$router.push('/user_register');
      },
    },
    styles: `
      .container {
        max-width: 600px;
      }
  
      .display-4 {
        color: #333;
      }
  
      .lead {
        color: #555;
      }
  
      .btn-primary,
      .btn-secondary {
        margin-top: 20px;
      }
    `,
  };
  