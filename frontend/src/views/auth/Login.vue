<template>
    <div class="sm:flex sm:flex-row flex flex-col flex-1">
        <div class="flex sm:flex-1 p-4 bg-catalina-blue-500 sm:rounded-tl-xl sm:rounded-bl-xl">
            <div class="flex flex-col text-catskill-white-100">
                <h1 class="font-archivo font-bold text-xl">
                    MalaDIS</h1>
                <div class="flex flex-col flex-1 justify-center text-center space-y-4">
                    <div class="font-paytone text-catalina-blue-50 sm:text-4xl text-md">Unlock Seamless Registration
                        Management</div>
                    <div class="sm:text-xl text-sm text-great-blue-200">
                        Experience hassle-free registration management with our user-centric system. Effortlessly
                        streamline the process, save time, and focus on what matters most. Welcome to the future of
                        simplicity and
                        efficiency.
                    </div>
                    <div class="text-lg">If you're new to <span class="text-catalina-blue-50 font-bold">MalaDIS</span>, sign
                        up for an account<span
                            class="rounded-2xl px-4 p-2 text-base bg-gradient-to-r from-catalina-blue-50 to-catalina-blue-300">Register</span>
                    </div>
                </div>
            </div>
        </div>
        <div class="flex flex-col justify-center sm:w-4/12 w-12/12 p-8 sm:border-l sm:border-l-athens-gray-400">
            <div class="flex flex-col sm:space-y-4 space-y-2">
                <div class=""><img class="w-32 h-32" src="@/assets/images/logo.png" /></div>
                <div class="font-bold text-catalina-blue-500 text-xl">Sign In</div>
                <div class="text-xl font-roboto-thin">Welcome back to your accout</div>
                <form class="flex flex-col space-y-4" @submit.prevent="submitLoginForm" method="POST">
                    <label class="block">
                        <span
                            class="after:content-['*'] after:ml-0.5 after:text-red-500 block text-sm font-medium text-slate-700">
                            Username
                        </span>
                        <input type="email" name="email" v-model="userData.username"
                            class="mt-2 p-3 bg-white border shadow-sm border-athens-gray-500 placeholder-slate-400 focus:outline-none focus:border-athens-gray-500 focus:border-athens-gray-500 block w-full rounded-xl sm:text-sm focus:ring-1"
                            placeholder="Email" required />
                    </label>
                    <label class="block">
                        <span
                            class="after:content-['*'] after:ml-0.5 after:text-red-500 block text-sm font-medium text-slate-700">
                            Password
                        </span>
                        <input type="password" name="password" v-model="userData.password"
                            class="mt-2 p-3 bg-white border shadow-sm border-athens-gray-500 placeholder-slate-400 focus:outline-none focus:border-athens-gray-500 focus:border-athens-gray-500 block w-full rounded-xl sm:text-sm focus:ring-1"
                            placeholder="Password" required />
                    </label>
                    <div class="flex space-between flex-row items-center">
                        <label class="relative inline-flex items-center cursor-pointer">
                            <input type="checkbox" value="" class="sr-only peer">
                            <div
                                class="w-11 h-6 bg-catskill-white-400 border-2 border-mid-gray-100 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-catalina-blue-200 dark:peer-focus:ring-catalina-blue-500 rounded-full peer dark:bg-athens-gray-700 peer-checked:after:translate-x-full peer-checked:after:border-catskill-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-mid-gray-100 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-mid-gray-500 peer-checked:bg-catalina-blue-100">
                            </div>
                            <span class="ml-3 text-sm font-bold dark:text-gray-200">Remember me</span>
                        </label>
                        <span class="flex-1 text-right hover:text-catalina-blue-500 font-bold text-sm">Forgot
                            Password?</span>
                    </div>
                    <div class="flex flex-row space-x-4">
                        <button type="submit"
                            class="mt-2 px-4 py-3 text-catskill-white-100 bg-gradient-to-r from-catalina-blue-300 to-catalina-blue-500 hover:bg-catalina-blue-400 rounded-xl">
                            Confirm
                        </button>
                        <div class="mt-2 px-3 py-3">Or <span class="font-bold text-catalina-blue-500">Create</span> an
                            account
                        </div>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<script>
import { login } from "@/services/authService";
import router from "@/router";
import { useAuthStore } from "@/store/authStore";

export default {
    name: "LoginView",
    data() {
        return {
            userData: {
                username: "",
                password: "",
            },
        };
    },
    methods: {
        async submitLoginForm() {
            try {
                const response = await login("/auth/login", this.userData);
                // saveTokenToLocalStorage(response.access_token);
                const authStore = useAuthStore();
                authStore.setUser(response.user);
                authStore.setPermissions(response.permissions);
                authStore.setAccessToken(response.access_token);
                router.push("/dashboard");
            } catch (error) {
                console.error("Error user login:", error);
            }
        },
    },
};
</script>
