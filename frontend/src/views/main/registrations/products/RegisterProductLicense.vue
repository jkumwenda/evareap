<template>
    <div class="flex flex-col space-y-4 flex-1">
        <HeaderView :headerTitle="headerTitle"></HeaderView>
        <div class="flex flex-row space-x-4">
            <div class="w-4/12 shadow-sm rounded-2xl bg-catskill-white-100">
                <router-link :to="{ name: 'YourRegistration' }"
                    class="block p-4 border-b text-catalina-blue-50 border-b-athens-gray-500 text-center hover:underline">
                    &laquo; Back to registration
                </router-link>
                <div class="p-5">
                    <div class="font-bold">4054826417</div>
                    <div class="flex flex-row text-sm space-x-2">
                        <p class="font-bold">ID:</p> 4054826417 | <p class="font-bold">Status:</p> Registration in progress
                    </div>
                </div>
                <div class="flex flex-col flex-1">
                    <div class="flex w-12/12 space-x-2 p-4 border-t border-t-athens-gray-500 items-center">
                        <CheckBadgeIcon class="w-8 h-8  text-spray-600"></CheckBadgeIcon>
                        <DocumentTextIcon class="w-5 h-5 text-mid-gray-200"></DocumentTextIcon>
                        <div>
                            <p>Personal Information</p>
                        </div>
                    </div>
                    <div class="flex w-12/12 space-x-2 p-4 border-t border-t-athens-gray-500 items-center">
                        <CheckBadgeIcon class="w-8 h-8  text-mid-gray-400"></CheckBadgeIcon>
                        <ArrowUpOnSquareIcon class="w-5 h-5 text-mid-gray-200"></ArrowUpOnSquareIcon>
                        <div>
                            <p>Product details</p>
                        </div>
                    </div>
                    <div class="flex w-12/12 space-x-2 p-4 border-t border-t-athens-gray-500 items-center">
                        <CheckBadgeIcon class="w-8 h-8  text-mid-gray-400"></CheckBadgeIcon>
                        <ArrowUpOnSquareIcon class="w-5 h-5 text-mid-gray-200"></ArrowUpOnSquareIcon>
                        <div>
                            <p>Manufacturer Infomation</p>
                        </div>
                    </div>
                    <div class="flex w-12/12 space-x-2 p-4 border-t border-t-athens-gray-500 items-center">
                        <CheckBadgeIcon class="w-8 h-8  text-mid-gray-400"></CheckBadgeIcon>
                        <ArrowUpOnSquareIcon class="w-5 h-5 text-mid-gray-200"></ArrowUpOnSquareIcon>
                        <div>
                            <p>License being applied for</p>
                        </div>
                    </div>
                </div>
                <div class="flex flex-col space-y-4 p-5 border-t border-t-athens-gray-500">
                    <div class="text-center">5 of 6 required tasks completed</div>
                    <div class="text-center border border-catalina-blue-50">
                        <div class="w-10/12 bg-catalina-blue-50 p-2"></div>
                    </div>
                    <div class="text-sm text-mid-gray-300 text-center">Last edited: 20 Oct 2023 11:23 PM (CAT)</div>
                    <div class="flex justify-between">
                        <button
                            class="p-3 px-8 uppercase text-sm font-bold rounded-2xl bg-catalina-blue text-catskill-white-400">Review</button>
                        <button
                            class="p-3 px-8 uppercase text-sm font-bold rounded-2xl bg-catalina-blue text-catskill-white-400">Submit</button>
                    </div>
                </div>
            </div>
            <div class="flex flex-col flex-1 shadow-sm rounded-2xl bg-catskill-white-100">
                <div class="flex w-12/12 text-xl space-x-2 p-4 border-b border-b-athens-gray-500 items-center">
                    <CheckBadgeIcon class="w-8 h-8  text-spray-200"></CheckBadgeIcon>
                    <DocumentTextIcon class="w-5 h-5 text-mid-gray-200"></DocumentTextIcon>
                    <div>
                        <p>Personal Information</p>
                    </div>
                </div>
                <div class="p-4">
                    <form class="flex-1 space-y-4 w-8/12">
                        <h1 class="flex font-bold text-lg space-x-4 items-center">
                            Basic Information:
                        </h1>
                        <label class="flex space-x-4 items-center">
                            <span class="text-sm w-4/12 font-medium text-slate-700">
                                Firstname
                            </span>
                            <input type="input" name="email"
                                class="mt-2 p-3 bg-white border shadow-sm border-athens-gray-500 placeholder-slate-400 focus:outline-none focus:border-athens-gray-500 focus:border-athens-gray-500 block w-full rounded-xl sm:text-sm focus:ring-1"
                                placeholder="Firstname..." required />
                        </label>
                        <label class="flex space-x-4 items-center">
                            <span class="text-sm w-4/12 font-medium text-slate-700">
                                Lastname
                            </span>
                            <input type="input" name="email"
                                class="mt-2 p-3 bg-white border shadow-sm border-athens-gray-500 placeholder-slate-400 focus:outline-none focus:border-athens-gray-500 focus:border-athens-gray-500 block w-full rounded-xl sm:text-sm focus:ring-1"
                                placeholder="Lastname..." required />
                        </label>
                        <label class="flex space-x-4 items-center">
                            <span class="text-sm w-4/12 font-medium text-slate-700">
                                Email
                            </span>
                            <input type="email" name="email"
                                class="mt-2 p-3 bg-white border shadow-sm border-athens-gray-500 placeholder-slate-400 focus:outline-none focus:border-athens-gray-500 focus:border-athens-gray-500 block w-full rounded-xl sm:text-sm focus:ring-1"
                                placeholder="Email..." required />
                        </label>
                        <label class="flex space-x-4 items-center">
                            <span class="text-sm w-4/12 font-medium text-slate-700">
                                Phone Number
                            </span>
                            <input type="email" name="phone"
                                class="mt-2 p-3 bg-white border shadow-sm border-athens-gray-500 placeholder-slate-400 focus:outline-none focus:border-athens-gray-500 focus:border-athens-gray-500 block w-full rounded-xl sm:text-sm focus:ring-1"
                                placeholder="Phone #..." required />
                        </label>
                        <h1 class="flex font-bold text-lg space-x-4 items-center">
                            Registering for:
                        </h1>
                        <label class="flex space-x-4 items-center">
                            <span class="text-sm w-4/12 font-medium text-slate-700">
                                License category
                            </span>
                            <select
                                class="mt-2 p-3 bg-white border shadow-sm border-athens-gray-500 placeholder-slate-400 focus:outline-none focus:border-athens-gray-500 focus:border-athens-gray-500 block w-full rounded-xl sm:text-sm focus:ring-1">
                                <option disabled>--Select license category--</option>
                                <option>Pharmacist</option>
                                <option>Pharmacy technician</option>
                            </select>
                        </label>
                        <h1 class="flex font-bold text-lg space-x-4 items-center">
                            Citizenship:
                        </h1>
                        <p class="text-sm">For administrative purposes.</p>
                        <label class="flex space-x-4 items-center">
                            <span class="text-sm w-4/12 font-medium text-slate-700">
                                Your Citizenship
                            </span>
                            <select
                                class="mt-2 p-3 bg-white border shadow-sm border-athens-gray-500 placeholder-slate-400 focus:outline-none focus:border-athens-gray-500 focus:border-athens-gray-500 block w-full rounded-xl sm:text-sm focus:ring-1">
                                <option disabled>--Select citizenship--</option>
                                <option>Malawi</option>
                                <option>Zambia</option>
                            </select>
                        </label>
                    </form>

                </div>
                <div class="flex space-x-4 p-4 border-t border-t-athens-gray-500 justify-center">
                    <button
                        class="p-3 px-8 bg-mid-gray-400 font-bold uppercase text-catskill-white-100 text-sm rounded-2xl">Save
                        &
                        continue
                        editing</button>
                    <button
                        class="p-3 px-8 bg-catalina-blue font-bold uppercase text-catskill-white-500 text-sm rounded-2xl">Mark
                        as complete</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import HeaderView from '@/includes/Header.vue'
import { CheckBadgeIcon, DocumentTextIcon, ArrowUpOnSquareIcon } from '@heroicons/vue/24/solid'
export default {
    name: 'RegisterProductLicenseView',
    components: {
        HeaderView, CheckBadgeIcon, DocumentTextIcon, ArrowUpOnSquareIcon
    },
    data() {
        return {
            headerTitle: "Product License Registration",
        }
    }
}
</script>
