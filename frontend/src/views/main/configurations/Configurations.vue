<template>
    <div class="flex flex-col space-y-4 flex-1">
        <HeaderView :headerTitle="headerTitle"></HeaderView>
        <SpinnerComponent v-if="isLoading" />
        <div v-else class="flex flex-wrap rounded-2xl bg-catskill-white-100 shadow-sm p-4">
            <router-link v-if="permissions.includes('VIEW_USER')" :to="{ name: 'Users' }"
                class="p-1 w-3/12 justify-center items-center text-center">
                <div
                    class="flex flex-row items-center p-4 rounded-2xl shadow-md bg-catskill-white-300 border border-catskill-white-500 cursor-pointer">
                    <UsersIcon class="h-8 w-8 font-light text-catalina-blue-100" />
                    <div class="pl-2">Users</div>
                </div>
            </router-link>
            <router-link v-if="permissions.includes('VIEW_ROLE')" :to="{ name: 'Roles' }"
                class="p-1 w-3/12 justify-center items-center text-center">
                <div
                    class="flex flex-row items-center p-4 rounded-2xl shadow-md bg-catskill-white-300 border border-catskill-white-500 cursor-pointer">
                    <UserGroupIcon class="h-8 w-8 font-light text-catalina-blue-100" />
                    <div class="pl-2">Roles</div>
                </div>
            </router-link>
            <router-link v-if="permissions.includes('VIEW_PRODUCT_CATEGORY')" :to="{ name: 'ProductCategories' }"
                class="p-1 w-3/12 justify-center items-center text-center">
                <div
                    class="flex flex-row items-center p-4 rounded-2xl shadow-md bg-catskill-white-300 border border-catskill-white-500 cursor-pointer">
                    <UserGroupIcon class="h-8 w-8 font-light text-catalina-blue-100" />
                    <div class="pl-2">Product Categories</div>
                </div>
            </router-link>
            <router-link v-if="permissions.includes('VIEW_THERAPEUTIC_CATEGORY')" :to="{ name: 'TherapeuticCategories' }"
                class="p-1 w-3/12 justify-center items-center text-center">
                <div
                    class="flex flex-row items-center p-4 rounded-2xl shadow-md bg-catskill-white-300 border border-catskill-white-500 cursor-pointer">
                    <UserGroupIcon class="h-8 w-8 font-light text-catalina-blue-100" />
                    <div class="pl-2">Therapeutic Categories</div>
                </div>
            </router-link>
            <router-link v-if="permissions.includes('VIEW_ADMINISTRATION_ROUTE')" :to="{ name: 'AdministrationRoutes' }"
                class="p-1 w-3/12 justify-center items-center text-center">
                <div
                    class="flex flex-row items-center p-4 rounded-2xl shadow-md bg-catskill-white-300 border border-catskill-white-500 cursor-pointer">
                    <UserGroupIcon class="h-8 w-8 font-light text-catalina-blue-100" />
                    <div class="pl-2">Administration Routes</div>
                </div>
            </router-link>
            <router-link v-if="permissions.includes('VIEW_GENERIC_NAME')" :to="{ name: 'GenericNames' }"
                class="p-1 w-3/12 justify-center items-center text-center">
                <div
                    class="flex flex-row items-center p-4 rounded-2xl shadow-md bg-catskill-white-300 border border-catskill-white-500 cursor-pointer">
                    <UserGroupIcon class="h-8 w-8 font-light text-catalina-blue-100" />
                    <div class="pl-2">Generic Names</div>
                </div>
            </router-link>
            <router-link v-if="permissions.includes('VIEW_DOSAGE_FORM')" :to="{ name: 'DosageForms' }"
                class="p-1 w-3/12 justify-center items-center text-center">
                <div
                    class="flex flex-row items-center p-4 rounded-2xl shadow-md bg-catskill-white-300 border border-catskill-white-500 cursor-pointer">
                    <UserGroupIcon class="h-8 w-8 font-light text-catalina-blue-100" />
                    <div class="pl-2">Dosage Form</div>
                </div>
            </router-link>
            <router-link v-if="permissions.includes('VIEW_WORKFLOW')" :to="{ name: 'Workflows' }"
                class="p-1 w-3/12 justify-center items-center text-center">
                <div
                    class="flex flex-row items-center p-4 rounded-2xl shadow-md bg-catskill-white-300 border border-catskill-white-500 cursor-pointer">
                    <UserGroupIcon class="h-8 w-8 font-light text-catalina-blue-100" />
                    <div class="pl-2">Workflows</div>
                </div>
            </router-link>
            <router-link v-if="permissions.includes('VIEW_PRODUCT_LICENCE_FEE')" :to="{ name: 'ProductLicenceFees' }"
                class="p-1 w-3/12 justify-center items-center text-center">
                <div
                    class="flex flex-row items-center p-4 rounded-2xl shadow-md bg-catskill-white-300 border border-catskill-white-500 cursor-pointer">
                    <UserGroupIcon class="h-8 w-8 font-light text-catalina-blue-100" />
                    <div class="pl-2">Product Licence Fees</div>
                </div>
            </router-link>
        </div>
    </div>
</template>

<script>
import HeaderView from '@/includes/Header.vue'
import SpinnerComponent from "@/components/Spinner.vue";
import { useAuthStore } from "@/store/authStore";
import {
    UsersIcon,
    UserGroupIcon,
    // CubeIcon,
    // OfficeBuildingIcon,
    // CollectionIcon,
    // DocumentIcon,
    // UserIcon,
    // CashIcon,
    // CogIcon
} from '@heroicons/vue/24/solid'

export default {
    name: 'ConfigurationsView',
    components: {
        HeaderView, SpinnerComponent,
        UsersIcon,
        UserGroupIcon,
        // CubeIcon,
        // OfficeBuildingIcon,
        // CollectionIcon,
        // DocumentIcon,
        // UserIcon,
        // CashIcon,
        // CogIcon,
    },
    setup() {
        const authStore = useAuthStore()
        const permissions = authStore.permissions
        return { permissions }
    },
}
</script>