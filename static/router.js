import home from './component/home.js'
import login from './component/login.js'
import admin_login from './component/admin_login.js'
import user_register from './component/user_register.js'
import admin_dash from './component/admin_dash.js'
import user_dash from './component/user_dash.js'
import artist_dash from './component/artist_dash.js'
import play from './component/play.js'
import manage_album from './component/manage_album.js'
import manage_song from './component/manage_song.js'




const routes = [
    {
        path: '/',
            component: home,
            beforeEnter: (to, from, next) => {
                const auth_token = localStorage.getItem('auth_token');
                const roles = localStorage.getItem('role');
            
                console.log('Auth Token:', auth_token);
                console.log('Roles:', roles);
            
                if (auth_token) {
                    if (roles.includes('admin')) {
                        console.log('Redirecting to admin_dash');
                        next('/admin_dash');
                    } else if (roles.includes('user')) {
                        console.log('Redirecting to user_dash');
                        next('/user_dash');
                    } else if (roles.includes('artist')) {
                        console.log('Redirecting to artist_dash');
                        next('/artist_dash');
                    } else {
                        console.log('Redirecting to default');
                        next();
                    }
                } else {
                    console.log('Redirecting to home');
                    next();
                }
            },
    },
    { path: '/user_login', component: login, name: 'login' },
    { path: '/admin_login', component: admin_login },
    { path: '/user_register', component: user_register },
    { path: '/admin_dash', component: admin_dash},
    { path: '/user_dash', component: user_dash},
    { path: '/artist_dash', component: artist_dash},
    { path: '/play', component: play},
    { path: '/api/manage_albums', component: manage_album},
    { path: '/api/manage_songs', component: manage_song},
];

export default new VueRouter({
    routes,
}) 