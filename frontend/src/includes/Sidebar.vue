<template>
    <div class="space-y-4">
        <ul class="space-y-1">
            <router-link :to="{ name: 'Dashboard' }"
                :class="{ 'text-catalina-blue-50 border-l-2 border-l-catalina-blue-50': $route.name === 'Dashboard' }"
                class="flex flex-row space-x-2 p-2 px-4  border-l-2 border-l-catalina-blue-50">
                <HomeIcon class="h-6 w-6" /><span>Home</span>
            </router-link>
        </ul>
        <div class="pt-4 pl-4 uppercase font-bold text-md">Manage Registration</div>
        <ul class="space-y-1">
            <router-link v-if="permissions.includes('VIEW_PERSONELL')" :to="{ name: 'PracticingLicenses' }"
                :class="{ 'flex flex-row space-x-2 p-2 px-4 text-catalina-blue-50 border-l-2 border-l-catalina-blue-50': $route.name === 'PracticingLicenses' }"
                class="flex flex-row space-x-2 p-2 px-4  border-l-2 border-l-catalina-blue-50">
                <UsersIcon class="h-6 w-6" /><span>Pharmacy Personnel</span>
            </router-link>
            <router-link v-if="permissions.includes('VIEW_PRODUCT')" :to="{ name: 'Products' }"
                :class="{ 'text-catalina-blue-50 border-l-2 border-l-catalina-blue-50': $route.name === 'Products' }"
                class="flex flex-row space-x-2 p-2 px-4 border-l-2 border-l-catalina-blue-50 hover:border-l-catalina-blue-50">
                <BeakerIcon class="h-6 w-6" /><span>Medicine Product</span>
            </router-link>
            <router-link v-if="permissions.includes('VIEW_APPLICANT')" :to="{ name: 'Applicants' }"
                :class="{ 'text-catalina-blue-50 border-l-2 border-l-catalina-blue-50': $route.name === 'Applicants' }"
                class="flex flex-row space-x-2 p-2 px-4 pl-8 border-l-2 border-l-catalina-blue-50 hover:border-l-catalina-blue-50">
                <DocumentTextIcon class="h-6 w-6" /><span>Applicants</span>
            </router-link>
            <router-link v-if="permissions.includes('VIEW_MANUFACTURER')" :to="{ name: 'Manufacturers' }"
                :class="{ 'text-catalina-blue-50 border-l-2 border-l-catalina-blue-50': $route.name === 'Manufacturers' }"
                class="flex flex-row space-x-2 p-2 px-4 pl-8 border-l-2 border-l-catalina-blue-50 hover:border-l-catalina-blue-50">
                <BuildingOffice2Icon class="h-6 w-6" /><span>Manufacturers</span>
            </router-link>
            <router-link v-if="permissions.includes('VIEW_BUSINESS')" :to="{ name: 'Businesses' }"
                :class="{ 'text-catalina-blue-50 border-l-2 border-l-catalina-blue-50': $route.name === 'Businesses' }"
                class="flex flex-row space-x-2 p-2 px-4 border-l-2 border-l-catalina-blue-50">
                <BuildingStorefrontIcon class="h-6 w-6" /><span>Pharmacy Business</span>
            </router-link>
            <router-link v-if="permissions.includes('VIEW_MY_REGISTRATION')" :to="{ name: 'YourRegistration' }"
                :class="{ 'text-catalina-blue-50 border-l-2 border-l-catalina-blue-50': $route.name === 'YourRegistration' }"
                class="flex flex-row space-x-2 p-2 px-4 border-l-2 border-l-catalina-blue-50">
                <UserIcon class="h-6 w-6" /><span>Your Registration</span>
            </router-link>
        </ul>
        <div class="pt-4 pl-4 uppercase font-black text-md">System Management</div>
        <ul class="space-y-1">
            <router-link :to="{ name: 'Users' }"
                :class="{ 'text-catalina-blue-50 border-l-2 border-l-catalina-blue-50': $route.name === 'Users' }"
                class="flex flex-row space-x-2 p-2 px-4 border-l-2 border-l-catalina-blue-50">
                <UserGroupIcon class="h-6 w-6" /><span>Users</span>
            </router-link>
            <router-link :to="{ name: 'Configurations' }"
                :class="{ 'text-catalina-blue-50 border-l-2 border-l-catalina-blue-50': $route.name === 'Configurations' }"
                class="flex flex-row space-x-2 p-2 px-4 border-l-2 border-l-catalina-blue-50">
                <Cog8ToothIcon class="h-6 w-6" /><span>Configuration</span>
            </router-link>
        </ul>
        <div
            class="flex flex-row space-x-2 rounded-2xl bg-catalina-blue-500 text-catskill-white-100 items-center m-4 p-4 py-4">
            <LifebuoyIcon class="w-10 h-10"></LifebuoyIcon>
            <span class="font-roboto-thin text-xl">Help</span>
        </div>
    </div>
</template>

<script>
import { HomeIcon, UserGroupIcon, UserIcon, Cog8ToothIcon, UsersIcon, BeakerIcon, BuildingStorefrontIcon, LifebuoyIcon, DocumentTextIcon, BuildingOffice2Icon } from '@heroicons/vue/24/solid'
import { useAuthStore } from "@/store/authStore";

export default {
    name: 'SidebarView',
    components: {
        HomeIcon, UsersIcon, UserIcon, UserGroupIcon, Cog8ToothIcon, BeakerIcon, BuildingStorefrontIcon, LifebuoyIcon, DocumentTextIcon, BuildingOffice2Icon
    },
    setup() {
        const authStore = useAuthStore()
        const permissions = authStore.permissions
        return { permissions }
    },
}
</script>