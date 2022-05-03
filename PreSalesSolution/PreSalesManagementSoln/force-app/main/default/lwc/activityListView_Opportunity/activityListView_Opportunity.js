import { api, LightningElement, track } from 'lwc';
import Id from "@salesforce/user/Id"
import { url } from 'c/dataUtils';

export default class ActivityListView_Opportunity extends LightningElement {
    @api opportunityId 

    connectedCallback() {
        this.fetchCurrentUser()
    }

    @track newActivityLabel = ''

    fetchCurrentUser() {
        const userID = Id ? Id : '0055f0000041g1mAAA'
        const urlString = url + 'member/' + userID + '/'

        fetch(urlString)
            .then(res => res.json())
            .then(user => {
                this.userProfile = user.user_role.name

                this.template.querySelector('c-sales-request-form').setAttribute('data-userprofile', this.userProfile)

                const userIsPresales = this.userProfile !== 'Sales Representative'
                this.newActivityLabel = userIsPresales ? 'Create a New Activity' : 'Request a New Activity'
            })
    }

    @track status = 'current'

    statusOptions = [
        {label: '--- All Activities/Requests ---', value: ''},
        {label: '--- All Current Activities/Requests ---', value: 'current'},
        {label: '--- All Accepted Activities ---', value: 'accepted'},
        {label: 'Unscheduled Activities', value: 'Accept'},
        {label: 'Scheduled Activities', value: 'Scheduled'},
        {label: '--- All Requests ---', value: 'requests'},
        {label: 'New Activity Requests', value: 'Request'},
        {label: 'Reschedule Requests', value: 'Reschedule'},
        {label: '--- All Past Activities ---', value: 'past'},
        {label: 'Completed Activities', value: 'Complete'},
        {label: 'Cancelled Activities', value: 'Cancel'},
        {label: 'Expired Activities', value: 'Expire'}
    ]

    selectStatus = (evt) => {
        this.status = evt.target.value

        let listView = this.template.querySelector('c-activity-list-view')

        listView.setAttribute('data-status', this.status)

        listView.loadTableRows()
    }

    get opportunityIdTesting () {
        return this.opportunityId ? this.opportunityId : '0065f000008xnXzAAI'
    }

    openRequestForm() {
        this.template.querySelector('c-sales-request-form').toggleModalClasses()
    }
}