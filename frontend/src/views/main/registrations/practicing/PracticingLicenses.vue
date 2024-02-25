<template>
    <div class="flex flex-col space-y-4 flex-1">
        <HeaderView :headerTitle="headerTitle"></HeaderView>
        <div class="flex flex-col space-y-4">
            <div class="">
                <SearchComponent></SearchComponent>
            </div>
            <div class="rounded-2xl bg-catskill-white-100 shadow-sm p-4">
                <div class="flex flex-row bg-athens-gray-500 p-2 text-sm font-bold">
                    <div class="sm:w-3/12">Firstname</div>
                    <div class="sm:w-3/12">Lastname</div>
                    <div class="sm:w-3/12">Reg #</div>
                    <div class="sm:w-2/12">Status</div>
                    <div class="sm:w-1/12">Action</div>
                </div>
                <div class="flex flex-row bg-athens-gray-400 p-2 text-sm items-center">
                    <div class="sm:w-3/12">Simon</div>
                    <div class="sm:w-3/12">Matchado</div>
                    <div class="sm:w-3/12">PMRA1234</div>
                    <div class="sm:w-2/12">Active</div>
                    <div class="flex space-x-2 sm:w-1/12">
                        <div class="p-1 bg-dodger-blue-50 rounded-full">
                            <EyeIcon class="w-5 h-5 text-catalina-blue-300"></EyeIcon>
                        </div>
                        <div class="p-1 bg-spray-200 rounded-full">
                            <PencilSquareIcon class="w-5 h-5 text-spray-700"></PencilSquareIcon>
                        </div>
                        <div class="p-1 bg-flamingo-100 rounded-full">
                            <TrashIcon class="w-5 h-5 text-flamingo-500"></TrashIcon>
                        </div>
                    </div>
                </div>
                <div class="flex flex-row bg-athens-gray-100 p-2 text-sm items-center">
                    <div class="sm:w-3/12">Mwiza</div>
                    <div class="sm:w-3/12">Kantungwe</div>
                    <div class="sm:w-3/12">PMRA2345</div>
                    <div class="sm:w-2/12">Active</div>
                    <div class="flex space-x-2 sm:w-1/12">
                        <div class="p-1 bg-dodger-blue-50 rounded-full">
                            <EyeIcon class="w-5 h-5 text-catalina-blue-300"></EyeIcon>
                        </div>
                        <div class="p-1 bg-spray-200 rounded-full">
                            <PencilSquareIcon class="w-5 h-5 text-spray-700"></PencilSquareIcon>
                        </div>
                        <div class="p-1 bg-flamingo-100 rounded-full">
                            <TrashIcon class="w-5 h-5 text-flamingo-500"></TrashIcon>
                        </div>
                    </div>
                </div>
                <div class="flex flex-row bg-athens-gray-400 p-2 text-sm items-center">
                    <div class="sm:w-3/12">Kelvin</div>
                    <div class="sm:w-3/12">Mwagomba</div>
                    <div class="sm:w-3/12">PMRA3456</div>
                    <div class="sm:w-2/12">Barred</div>
                    <div class="flex space-x-2 sm:w-1/12">
                        <div class="p-1 bg-dodger-blue-50 rounded-full">
                            <EyeIcon class="w-5 h-5 text-catalina-blue-300"></EyeIcon>
                        </div>
                        <div class="p-1 bg-spray-200 rounded-full">
                            <PencilSquareIcon class="w-5 h-5 text-spray-700"></PencilSquareIcon>
                        </div>
                        <div class="p-1 bg-flamingo-100 rounded-full">
                            <TrashIcon class="w-5 h-5 text-flamingo-500"></TrashIcon>
                        </div>
                    </div>
                </div>

                <div class="flex flex-row bg-athens-gray-100 p-2 text-sm items-center">
                    <div class="sm:w-3/12">Mercy</div>
                    <div class="sm:w-3/12">Sitima</div>
                    <div class="sm:w-3/12">PMRA4567</div>
                    <div class="sm:w-2/12">Suspended</div>
                    <div class="flex space-x-2 sm:w-1/12">
                        <div class="p-1 bg-dodger-blue-50 rounded-full">
                            <EyeIcon class="w-5 h-5 text-catalina-blue-300"></EyeIcon>
                        </div>
                        <div class="p-1 bg-spray-200 rounded-full">
                            <PencilSquareIcon class="w-5 h-5 text-spray-700"></PencilSquareIcon>
                        </div>
                        <div class="p-1 bg-flamingo-100 rounded-full">
                            <TrashIcon class="w-5 h-5 text-flamingo-500"></TrashIcon>
                        </div>
                    </div>
                </div>
                <div class="flex flex-row bg-athens-gray-400 p-2 text-sm items-center">
                    <div class="sm:w-3/12">Koma</div>
                    <div class="sm:w-3/12">Masiye</div>
                    <div class="sm:w-3/12">PMRA5678</div>
                    <div class="sm:w-2/12">Active</div>
                    <div class="flex space-x-2 sm:w-1/12">
                        <div class="p-1 bg-dodger-blue-50 rounded-full">
                            <EyeIcon class="w-5 h-5 text-catalina-blue-300"></EyeIcon>
                        </div>
                        <div class="p-1 bg-spray-200 rounded-full">
                            <PencilSquareIcon class="w-5 h-5 text-spray-700"></PencilSquareIcon>
                        </div>
                        <div class="p-1 bg-flamingo-100 rounded-full">
                            <TrashIcon class="w-5 h-5 text-flamingo-500"></TrashIcon>
                        </div>
                    </div>
                </div>
                <PaginationComponent></PaginationComponent>
            </div>
        </div>
    </div>
</template>

<script>
import HeaderView from '@/includes/Header.vue'
import { EyeIcon, PencilSquareIcon, TrashIcon } from '@heroicons/vue/24/solid'
import PaginationComponent from '@/components/PaginationComponent.vue'
import SearchComponent from '@/components/SearchComponent.vue'

export default {
    name: 'PracticingLicensesView',
    components: {
        EyeIcon, PencilSquareIcon, TrashIcon, PaginationComponent, SearchComponent, HeaderView
    },
    data() {
        return {
            headerTitle: "Practicing Licenses",
        }
    }
}
</script>