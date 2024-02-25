<template>
    <div class="flex flex-col space-y-4 flex-1">
        <HeaderView :headerTitle="headerTitle"></HeaderView>
        <div class="flex flex-col space-y-4">
            <div class="flex flex-row space-x-4">
                <div class="flex flex-col space-y-4 bg-catskill-white-50 p-4 sm:w-6/12 rounded-2xl shadow-sm flex-1">
                    <span class="text-md font-bold">Your quick stats</span>
                    <div class="flex flex-row flex-wrap">
                        <div class="w-1/2">
                            <div class="flex flex-row bg-athens-gray-400 m-2 p-4 py-6 rounded-xl space-x-4 items-center">
                                <div class="p-2 rounded-full bg-dodger-blue-50">
                                    <PresentationChartLineIcon class="w-6 h-6 text-catalina-blue-500">
                                    </PresentationChartLineIcon>
                                </div>
                                <div class="flex flex-col">
                                    <span class="text-md font-bold">154</span>
                                    <span class="text-sm font-roboto-thin font-bold text-mid-gray-300">New
                                        registrations</span>
                                </div>
                            </div>
                        </div>
                        <div class="w-1/2">
                            <div class="flex flex-row bg-athens-gray-400 m-2 p-4 py-6 rounded-xl space-x-4 items-center">
                                <div class="p-2 rounded-full bg-seance-100">
                                    <HandThumbUpIcon class="w-6 h-6 text-seance-500">
                                    </HandThumbUpIcon>
                                </div>
                                <div class="flex flex-col">
                                    <span class="text-md font-bold">17</span>
                                    <span class="text-sm font-roboto-thin font-bold text-mid-gray-300">Pending
                                        registrations</span>
                                </div>
                            </div>
                        </div>
                        <div class="w-1/2">
                            <div class="flex flex-row bg-athens-gray-400 m-2 p-4 py-6 rounded-xl space-x-4 items-center">
                                <div class="p-2 rounded-full bg-buttercup-50">
                                    <HandThumbUpIcon class="w-6 h-6 text-buttercup-500">
                                    </HandThumbUpIcon>
                                </div>
                                <div class="flex flex-col">
                                    <span class="text-md font-bold">870</span>
                                    <span class="text-sm font-roboto-thin font-bold text-mid-gray-300">Medicines</span>
                                </div>
                            </div>
                        </div>
                        <div class="w-1/2">
                            <div class="flex flex-row bg-athens-gray-400 m-2 p-4 py-6 rounded-xl space-x-4 items-center">
                                <div class="p-2 rounded-full bg-spray-200">
                                    <BanknotesIcon class="w-6 h-6 text-spray-700">
                                    </BanknotesIcon>
                                </div>
                                <div class="flex flex-col">
                                    <span class="text-md font-bold">MWK 287 Million</span>
                                    <span class="text-sm font-roboto-thin font-bold text-mid-gray-300">Revenue</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="fflex flex-col space-y-4 bg-catskill-white-50 p-4 sm:w-6/12 rounded-2xl shadow-sm flex-1">
                    <span class="text-md font-bold">Licesese registration status</span>
                    <img src="@/assets/images/graph.png" />
                </div>
            </div>
            <div class="flex flex-row space-x-4">
                <div
                    class="flex flex-col flex-1 p-4 bg-catalina-blue rounded-2xl text-catskill-white-500 text-center items-center justify-center">
                    <h1 class="text-lg font-bold">Manage your Registration</h1>
                    <p class="font-roboto-thin">- Check your license status -</p>
                    <p class="font-roboto-thin">- Renewal your license -</p>
                    <p class="font-roboto-thin">- Request for help -</p>
                </div>
                <div class="flex-1 space-y-4 bg-catskill-white-50 p-4 sm:w-6/12 rounded-2xl shadow-sm flex-1">
                    <span class="text-md font-bold">License renewal status</span>
                    <div class="flex flex-1 items-center justify-center">
                        <img src="@/assets/images/license.png" />
                    </div>
                </div>
                <div class="flex-1 space-y-4 bg-catskill-white-50 p-4 sm:w-6/12 rounded-2xl shadow-sm flex-1">
                    <span class="text-md font-bold">Fee collection evolution</span>
                    <div class="flex flex-1 items-center justify-center">
                        <img class="w-60" src="@/assets/images/fee.png" />
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import HeaderView from '@/includes/Header.vue'
import { PresentationChartLineIcon, HandThumbUpIcon, BanknotesIcon } from '@heroicons/vue/24/solid'

export default {
    name: 'DashboardView',
    components: {
        PresentationChartLineIcon, HandThumbUpIcon, BanknotesIcon, HeaderView
    },
    data() {
        return {
            headerTitle: "Dashboard",
        }
    }
}
</script>