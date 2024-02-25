<template>
    <div class="flex flex-col space-y-4 flex-1">
        <HeaderView :headerTitle="headerTitle"></HeaderView>
        <div class="flex flex-row space-x-4">
            <div class="w-4/12 shadow-sm p-4 rounded-2xl bg-catskill-white-100 space-y-4">
                <h1 class="font-bold text-xl">New registration</h1>
                <router-link :to="{ name: 'RegisterPracticingLicense' }"
                    class="p-4 block text-catskill-white-100 bg-gradient-to-r from-catalina-blue-200 to-catalina-blue-100 hover:from-catalina-blue-100 hover:to-catalina-blue-200 rounded-2xl">
                    Practicing License</router-link>
                <div
                    class="p-4 block text-catskill-white-100 bg-gradient-to-r from-catalina-blue-200 to-catalina-blue-100 hover:from-catalina-blue-100 hover:to-catalina-blue-200 rounded-2xl">
                    Business License</div>
                <router-link :to="{ name: 'RegisterProductLicense' }"
                    class="p-4 block text-catskill-white-100 bg-gradient-to-r from-catalina-blue-200 to-catalina-blue-100 hover:from-catalina-blue-100 hover:to-catalina-blue-200 rounded-2xl">
                    Product License</router-link>
            </div>
            <div class="flex flex-1 shadow-sm p-4 rounded-2xl bg-catskill-white-100 items-center justify-center">
                <p>No any registrations available create a new one !</p>
            </div>
        </div>
    </div>
</template>

<script>
import HeaderView from '@/includes/Header.vue'

export default {
    name: 'YourRegistration',
    components: {
        HeaderView
    },
    data() {
        return {
            headerTitle: "Your Registration",
        }
    }
}
</script>