<template>
    <div class="flex flex-row p-4 bg-catalina-blue rounded-2xl">
        <div class="flex flex-row flex-1 justify-between space-x-2 items-center">
            <div class="flex flex-row items-center space-x-4">
                <Bars3CenterLeftIcon class="h-8 w-8 text-catalina-blue-50" />
                <span class="text-lg text-catskill-white-500">{{ headerTitle }}</span>
            </div>
            <div class="flex items-center space-x-4 justify-end">
                <div class="flex flex-row items-center">
                    <BellIcon class="w-6 h-6 text-catalina-blue-50"></BellIcon>
                </div>
                <div class="flex flex-row items-center">
                    <EnvelopeIcon class="w-6 h-6 text-catalina-blue-50"></EnvelopeIcon>
                </div>
                <ProfileComponent :label="`${firstname} ${lastname}`"></ProfileComponent>
            </div>
        </div>
    </div>
</template>

<script>
import { Bars3CenterLeftIcon, EnvelopeIcon, BellIcon } from '@heroicons/vue/24/solid'
import ProfileComponent from "@/components/ProfileComponent";
export default {
    name: "HeaderView",
    components: {
        Bars3CenterLeftIcon, BellIcon, EnvelopeIcon, ProfileComponent
    },
    props: {
        headerTitle: String,
    }
}
</script>