odoo.define('account_extend_ikatech.main', function (require) {

    const AbstractAction = require('web.AbstractAction');
    const core = require('web.core');

    var rpc = require('web.rpc');
    var QWeb = core.qweb;
    var time = require('web.time');

    const dateComparations = () => {
        var dateComparation = {}
        var comDateTo = document.querySelector('#comparation_date_to')
        var comDateFrom = document.querySelector('#comparation_date_from')
        if (comDateTo.value  && comDateFrom.value){
            dateComparation.date_to = comDateTo.value
            dateComparation.date_from = comDateFrom.value
            document.querySelector("#comparation").checked = true
        };
        return dateComparation;
    };

    const OurAction = AbstractAction.extend({
        template: "account_extend_ikatech.ClientAction",  

        events: {
            'click #apply_filter': 'apply_filter',
            'click #pdf': 'print_pdf',
            'click #xlsx': 'print_xlsx',
            'click .view_purchase_order': 'button_view_order',
            'click .pr-line': 'show_drop_down',
            'click .third_line': 'show_detail_lines',
            'click #action_see_more': 'action_see_more',
            'click .fourth_line': 'show_analytics_account',
            'click #action_see_more_analytic': 'action_see_more_analytic',
            'click #comparation': 'show_box_comparation',
            'click #comparation_button': 'show_filters_comparation',
            'change #months': 'active_comparation',
            'change #years': 'active_comparation_years',
            'change #monthYear': 'active_comparation_years_month',
            'click #setDates': 'show_box_dates',
            'click .fourthDetailAmount': 'action_see_more_fourth',
            'click #monthComparation': 'monthComparation',
            'click #yearsComparation': 'yearsComparation',
            'click #datesComparation': 'datesComparation',
            'click #monthYearComparation': 'monthYearComparation',
            'click #date_custom':  'showDateCustmom',
            'click #thisMonth': "setThisMonth",
            'click #thisSemester': "setThisSemester",
            'click #thisYear': "setThisYear",
            'click #lastMonth': "setLastMonth",
            'click #lastSemester': "setLastSemester",
            'click #lastYear': "setLastYear",
        },

        //! default functions
        init: function(parent, action) {
            this._super(parent, action);
            this.company_id = action.context.allowed_company_ids[0];
            this.wizard_id = action.context.wizard | null;
        },

        start: function() {
            var self = this;
            self.initial_render = true;
            rpc.query({
                model: 'account.reports.pandl',
                method: 'create',
                args: [{
                }]
            }).then(function(res) {
                self.wizard_id = res;
                self.load_data(self.initial_render);
            })
        },

        load_data: function(initial_render = true) {
            var self = this;
            var comparation = false;
            var months = 0;
            var years = 0;
            var monthYear = 0
            var dateComparation = {}
            const filter_data_selected = {};
            if (initial_render) {
                filter_data_selected.date_from = moment().format('YYYY-MM-DD');
                filter_data_selected.date_to = moment().startOf('year').format('YYYY-MM-DD');
                // filter_data_selected.date_to = moment(date_to, time.getLangDateFormat()).locale('en').format('YYYY-MM-DD');
            } else {
                filter_data_selected.date_from = moment(new Date(this.$el.find('.datetimepicker-input[name="date_from"]').val()+"T00:00:00"), time.getLangDateFormat()).locale('en').format('YYYY-MM-DD');
                filter_data_selected.date_to = moment(new Date(this.$el.find('.datetimepicker-input[name="date_to"]').val()+"T00:00:00"), time.getLangDateFormat()).locale('en').format('YYYY-MM-DD');
                months = self.el.querySelector('#months').value
                years = self.el.querySelector('#years').value
                monthYear = self.el.querySelector('#monthYear').value
                dateComparation = dateComparations()
                comparation = self.el.querySelector('#comparation').checked
                console.log(dateComparation)
            }
            self._rpc({
                model: 'account.reports.pandl',
                method: 'pandl_report',
                args: [
                    [this.wizard_id, this.company_id, filter_data_selected, comparation, months, years, monthYear, dateComparation], 
                ],
            }).then(function(datas) {
                if (initial_render) {
                    self.$('.filter_view_pandl').html(QWeb.render('analyticPandlFilterView', {
                        filter_data: datas['filters'],
                    }));
                    self.el.querySelector('.datetimepicker-input[name="date_from"]').value = moment().format('YYYY-MM-DD');
                    self.el.querySelector('.datetimepicker-input[name="date_to"]').value =  moment().startOf('year').format('YYYY-MM-DD');
                }
                if (datas['orders']) {
                    self.$('.table_view_pr').html(QWeb.render('analyticPandlTable', {
                        filter: datas['filters'],
                        order: datas['orders'],
                        comparation: datas['comparation'],
                        data_report: datas['data_report'],
                        dates_name: datas['dates_name'],
                    }));
                } 
            })
        },

        //! Data functions
        apply_filter: function() {
            var self = this;
            self.initial_render = false;
            var filter_data_selected = {};
            filter_data_selected.date_from = moment(new Date(this.$el.find('.datetimepicker-input[name="date_from"]').val()+"T00:00:00"), time.getLangDateFormat()).locale('en').format('YYYY-MM-DD');
            filter_data_selected.date_to = moment(new Date(this.$el.find('.datetimepicker-input[name="date_to"]').val()+"T00:00:00"), time.getLangDateFormat()).locale('en').format('YYYY-MM-DD');
            var self = this;
            let elComp = self.el.querySelector("#boxComparationCont")
            elComp.setAttribute("hidden", "hidden");
            let elDate = self.el.querySelector("#boxSetDates")
            elDate.setAttribute("hidden", "hidden");

            rpc.query({
                model: 'account.reports.pandl',
                method: 'write',
                args: [
                self.wizard_id, filter_data_selected
                ],
            }).then(function(res) {
                self.initial_render = false;
                self.load_data(self.initial_render);
            });;
        },

        show_detail_lines: function(element) {
            var self = this;
            const typeOp = element.target.getAttribute("typeop")
            const idRow = element.target.getAttribute("idRow")
            const months = self.el.querySelector('#months').value
            const years = self.el.querySelector('#years').value
            const monthYear = self.el.querySelector('#monthYear').value
            const dateComparation = dateComparations()
            const comparation = self.el.querySelector('#comparation').checked
            const date_from = moment(new Date(this.$el.find('.datetimepicker-input[name="date_from"]').val()+"T00:00:00"), time.getLangDateFormat()).locale('en').format('YYYY-MM-DD');
            const date_to = moment(new Date(this.$el.find('.datetimepicker-input[name="date_to"]').val()+"T00:00:00"), time.getLangDateFormat()).locale('en').format('YYYY-MM-DD');
            
            if (self.$(`.detail_lines.${typeOp}`).length > 0){
                const incomesLines = self.el.querySelectorAll(`.detail_lines.${typeOp}`);
                for (let i = 0; i < incomesLines.length; i++){
                    incomesLines[i].remove();
                };
                if (self.el.querySelectorAll(`.detailAccountFourth.${typeOp}`).length > 0){
                    self.el.querySelectorAll(`.detailAccountFourth.${typeOp}`).forEach(e => e.remove());
                }
            } else {
                rpc.query({
                    model: 'account.reports.pandl',
                    method: 'get_details_lines',
                    args: [self.wizard_id, self.company_id, typeOp, idRow, date_from, date_to, comparation, months, years, monthYear, dateComparation],
                }).then(function(datas) {
                    var htmlString = ""
                    var aml = ['depre','amort','net_incomes','customer_comissions','other_incomes','costo_directo_op','otros_costos_op','comision_brokers']
                    if (aml.includes(datas['type_operation'])) {
                        datas['data'].forEach((e) => {
                            htmlString += `<tr id="rowAccount_${e.id}" class="detail_lines ${datas['type_operation']}">
                                <th>
                                    <a class="fourth_line">
                                        <span class="title_subline cursorPointer" idaccount="${e.id}" type_operation="${datas['type_operation']}">
                                            <i class="accuntShowDetail${e.id} fa fa-caret-right" role="img" aria-label="Desplegado" title="Desplegado"></i>
                                            ${e.name}
                                        </span>
                                    </a>
                                </th>`
                            for (var i = 0; i < e.amount.length; i++ ){
                                htmlString += `<th><span class="DetailAmount" id="action_see_more" idAccount="${e.id}" class="detailAmont"
                                    date_from="${datas['dates'][i].date_from}" date_to="${datas['dates'][i].date_to}">${e.amount[i]}</span></th>`
                            }
                            htmlString +=`</tr>`
                        });
                    } else {
                        datas['data'].forEach((e) => {
                            htmlString += `<tr id="rowAccount_${e.id}" class="detail_lines ${datas['type_operation']}">
                                            <th>
                                                <a>
                                                    <span class="title_subline" idaccount="${e.id}">${e.name}</span>
                                                </a>
                                            </th>`
                            for (var i = 0; i < e.amount.length; i++ ){
                                htmlString += `<th>
                                                <span class="DetailAmount " id="action_see_more_analytic" 
                                                    idAccount="${e.id}" 
                                                    date_from="${datas['dates'][i].date_from}" date_to="${datas['dates'][i].date_to}"
                                                    type_operation="${datas['type_operation']}">${e.amount[i]}</span>
                                                </th>`
                            }
                            htmlString +=`</tr>`
                        });
                    }
                    self.el.querySelector(`#${datas['idRow']}`).insertAdjacentHTML('afterend', htmlString);
                    // Viñeta de la lista
                    if (self.el.querySelector(`.third_line[typeop="${datas['type_operation']}"] .fa-caret-right`)){
                        self.el.querySelector(`.third_line[typeop="${datas['type_operation']}"] .fa-caret-right`).classList.replace("fa-caret-right", "fa-caret-down");
                    } else {
                        self.el.querySelector(`.third_line[typeop="${datas['type_operation']}"] .fa-caret-down`).classList.replace("fa-caret-down", "fa-caret-right");
                    }
                })
            }
        },

        action_see_more: function(element) {
            var self = this;
            var accountId = element.target.getAttribute("idAccount")
            const date_from = moment(new Date(element.target.getAttribute("date_from")+"T00:00:00"), time.getLangDateFormat()).locale('en').format('YYYY-MM-DD');
            const date_to = moment(new Date(element.target.getAttribute("date_to")+"T00:00:00"), time.getLangDateFormat()).locale('en').format('YYYY-MM-DD');

            self._rpc({
                model: 'account.reports.pandl',
                method: 'show_detail_data',
                args: [ accountId, date_from, date_to ],
                context: self.odoo_context,
            })
            .then(function(result){
                return self.do_action(result);
            })
        },

        action_see_more_analytic: function(element) {
            var self = this;
            var accountId = element.target.getAttribute("idAccount")
            var type_operation = element.target.getAttribute("type_operation")
            const date_from = moment(new Date(element.target.getAttribute("date_from")+"T00:00:00"), time.getLangDateFormat()).locale('en').format('YYYY-MM-DD');
            const date_to = moment(new Date(element.target.getAttribute("date_to")+"T00:00:00"), time.getLangDateFormat()).locale('en').format('YYYY-MM-DD');

            self._rpc({
                model: 'account.reports.pandl',
                method: 'show_detail_data_analytic',
                args: [ accountId, self.company_id, date_from, date_to, type_operation],
                context: self.odoo_context,
            })
            .then(function(result){
                return self.do_action(result);
            })
        },
        
        show_analytics_account: function(el) {
            var self = this;
            const months = self.el.querySelector('#months').value
            const years = self.el.querySelector('#years').value
            const monthYear = self.el.querySelector('#monthYear').value
            const dateComparation = dateComparations()
            const accountId = el.target.getAttribute("idaccount") //por alguna razon trae la equiqueta span hija
            var type_operation = el.target.getAttribute("type_operation")
            const comparation = self.el.querySelector('#comparation').checked
            const date_from = moment(new Date(this.$el.find('.datetimepicker-input[name="date_from"]').val()+"T00:00:00"), time.getLangDateFormat()).locale('en').format('YYYY-MM-DD');
            const date_to = moment(new Date(this.$el.find('.datetimepicker-input[name="date_to"]').val()+"T00:00:00"), time.getLangDateFormat()).locale('en').format('YYYY-MM-DD');
            
            if (self.$(`.detailAccount${accountId}`).length > 0){
                const incomesLines = self.$(`.detailAccount${accountId}`);
                for (let i = 0; i < incomesLines.length; i++){
                    incomesLines[i].remove();
                }
            } else {
                rpc.query({
                    model: 'account.reports.pandl',
                    method: 'get_analytics_account',
                    args: [self.wizard_id, self.company_id, accountId, date_from, date_to, comparation, months, years, monthYear, dateComparation],
                }).then(function(datas) {
                    var htmlString = ""
                    datas['data'].forEach((e) => {
                        htmlString += `<tr class="detailAccount${datas['idAccount']} detailAccountFourth ${type_operation}">
                            <th>
                                <a class="fourthDetailLine">
                                    ${e.name}
                                </a>
                            </th>`
                        for (var i = 0; i < e.amount.length; i++ ){
                            htmlString += `<th><a class="fourthDetailAmount" style="cursor: pointer;" 
                                                idAccount="${datas['idAccount']}"
                                                idAnalytic="${e.id}"
                                                date_from="${datas['dates'][i].date_from}" 
                                                date_to="${datas['dates'][i].date_to}">${e.amount[i]}</a>
                                            </th>`
                        }
                        htmlString +=`</tr>`
                    });
                    self.el.querySelector(`#rowAccount_${datas['idAccount']}`).insertAdjacentHTML('afterend', htmlString);

                    if (self.el.querySelector(`.accuntShowDetail${datas['idAccount']}.fa-caret-right`)){
                        self.el.querySelector(`.accuntShowDetail${datas['idAccount']}.fa-caret-right`).classList.replace("fa-caret-right", "fa-caret-down");
                    } else {
                        self.el.querySelector(`.accuntShowDetail${datas['idAccount']}.fa-caret-down`).classList.replace("fa-caret-down", "fa-caret-right");
                    }
                });  
            }        
        },

        action_see_more_fourth: function(element) {
            var self = this;
            var accountId = element.target.getAttribute("idAccount")
            var idAnalytic = element.target.getAttribute("idAnalytic")
            const date_from = moment(new Date(element.target.getAttribute("date_from")+"T00:00:00"), time.getLangDateFormat()).locale('en').format('YYYY-MM-DD');
            const date_to = moment(new Date(element.target.getAttribute("date_to")+"T00:00:00"), time.getLangDateFormat()).locale('en').format('YYYY-MM-DD');

            self._rpc({
                model: 'account.reports.pandl',
                method: 'show_amount_analytic_detail',
                args: [ accountId, date_from, date_to, idAnalytic],
                context: self.odoo_context,
            })
            .then(function(result){
                return self.do_action(result);
            })
        },

        //! Frontend views
        show_box_dates: function(){
            var self = this;
            let element = self.el.querySelector("#boxSetDates")
            let hidden = element.getAttribute("hidden");
            if (hidden) {
                element.removeAttribute("hidden");
            } else {
                element.setAttribute("hidden", "hidden");
            }
        },

        active_comparation: function() {
            var self = this;
            let check = self.el.querySelector("#comparation")
            let months = self.el.querySelector("#months")
            if (months.value == 0){
                check.checked = false
            } else {
                check.checked = true
            }
        },

        active_comparation_years: function() {
            var self = this;
            let check = self.el.querySelector("#comparation")
            let years = self.el.querySelector("#years")
            if (years.value == 0){
                check.checked = false
            } else {
                check.checked = true
            }
        },

        active_comparation_years_month: function() {
            var self = this;
            let check = self.el.querySelector("#comparation")
            let years = self.el.querySelector("#monthYear")
            if (years.value == 0){
                check.checked = false
            } else {
                check.checked = true
            }
        },

        show_filters_comparation: function (e) {
            var self = this;
            let element = self.el.querySelector("#boxComparationCont")
            let hidden = element.getAttribute("hidden");
                if (hidden) {
                element.removeAttribute("hidden");
            } else {
                element.setAttribute("hidden", "hidden");
            }
        },
        
        show_box_comparation: function(e) {
            var self = this;
            let element = self.el.querySelector("#boxComparationCont")
            let hidden = element.getAttribute("hidden");
            if (hidden) {
                element.removeAttribute("hidden");
            } else {
                element.setAttribute("hidden", "hidden");
            }
        },

        showDateCustmom: function(e){
            var self = this;
            let element = self.el.querySelector(".box-inside-dates")
            let hidden = element.getAttribute("hidden");
            if (hidden) {
                element.removeAttribute("hidden");
            } else {
                element.setAttribute("hidden", "hidden");
            }
        },

        yearsComparation: function(e){
            var self = this;
            let element = self.el.querySelector("#year_box_comparation")
            let hidden = element.getAttribute("hidden");
            if (hidden) {
                element.removeAttribute("hidden");
            } else {
                element.setAttribute("hidden", "hidden");
                let year = self.el.querySelector("#years");
                year.value = 0
            }
        },

        monthComparation: function(e){
            var self = this;
            let element = self.el.querySelector("#months_box_comparation")
            let hidden = element.getAttribute("hidden");
            if (hidden) {
                element.removeAttribute("hidden");
            } else {
                element.setAttribute("hidden", "hidden");
                let months = self.el.querySelector("#months");
                months.value = 0
            }
        },

        monthYearComparation: function(e){
            var self = this;
            let element = self.el.querySelector("#year_month_box_comparation")
            let hidden = element.getAttribute("hidden");
            if (hidden) {
                element.removeAttribute("hidden");
            } else {
                element.setAttribute("hidden", "hidden");
                let months = self.el.querySelector("#monthYear");
                months.value = 0
            }
        },

        datesComparation: function(e){
            var self = this;
            let element = self.el.querySelector("#dates_box_comparation")
            let hidden = element.getAttribute("hidden");
            if (hidden) {
                element.removeAttribute("hidden");
            } else {
                element.setAttribute("hidden", "hidden");
                self.el.querySelector('#comparation_date_to').value = ''
                self.el.querySelector('#comparation_date_from').value = ''
            }
        },

        // ! Dates Frontend
        setLastYear: function() {
            var self = this;
            const firstdate = moment().subtract(1, 'Year').startOf('Year').format('YYYY-MM-DD');
            const lastdate = moment().subtract(1, 'Year').endOf('Year').format("YYYY-MM-DD");
            var dateFrom = self.el.querySelector('.datetimepicker-input[name="date_from"]')
            dateFrom.value = lastdate
            var dateTo = self.el.querySelector('.datetimepicker-input[name="date_to"]')
            dateTo.value = firstdate
            var checkDate = self.el.querySelector('#checkDate');
            checkDate.remove()
            var btn = self.el.querySelector('#lastYear')
            var icon = document.createElement('i');
            icon.className = 'fa fa-solid fa-check'
            icon.style = 'color: #28a745;'
            icon.id = 'checkDate'
            btn.firstChild.before(icon);
        },

        setLastSemester: function() {
            var self = this;
            const firstdate = moment().subtract(1, 'quarter').startOf('quarter').format('YYYY-MM-DD');
            const lastdate = moment().subtract(1, 'quarter').endOf('quarter').format("YYYY-MM-DD");
            var dateFrom = self.el.querySelector('.datetimepicker-input[name="date_from"]')
            dateFrom.value = lastdate
            var dateTo = self.el.querySelector('.datetimepicker-input[name="date_to"]')
            dateTo.value = firstdate
            var checkDate = self.el.querySelector('#checkDate');
            checkDate.remove()
            var btn = self.el.querySelector('#lastSemester')
            var icon = document.createElement('i');
            icon.className = 'fa fa-solid fa-check'
            icon.style = 'color: #28a745;'
            icon.id = 'checkDate'
            btn.firstChild.before(icon);
        },


        setLastMonth: function() {
            var self = this;
            const firstdate = moment().subtract(1, 'month').startOf('month').format('YYYY-MM-DD');
            const lastdate = moment().subtract(1, 'month').endOf('month').format("YYYY-MM-DD");
            var dateFrom = self.el.querySelector('.datetimepicker-input[name="date_from"]')
            dateFrom.value = lastdate
            var dateTo = self.el.querySelector('.datetimepicker-input[name="date_to"]')
            dateTo.value = firstdate
            var checkDate = self.el.querySelector('#checkDate');
            checkDate.remove()
            var btn = self.el.querySelector('#lastMonth')
            var icon = document.createElement('i');
            icon.className = 'fa fa-solid fa-check'
            icon.style = 'color: #28a745;'
            icon.id = 'checkDate'
            btn.firstChild.before(icon);
        },

        setThisYear: function() {
            var self = this;
            const firstdate = moment().startOf('Year').format('YYYY-MM-DD');
            const lastdate = moment().endOf('Year').format("YYYY-MM-DD");
            var dateFrom = self.el.querySelector('.datetimepicker-input[name="date_from"]')
            dateFrom.value = lastdate
            var dateTo = self.el.querySelector('.datetimepicker-input[name="date_to"]')
            dateTo.value = firstdate
            var checkDate = self.el.querySelector('#checkDate');
            checkDate.remove()
            var btn = self.el.querySelector('#thisYear')
            var icon = document.createElement('i');
            icon.className = 'fa fa-solid fa-check'
            icon.style = 'color: #28a745;'
            icon.id = 'checkDate'
            btn.firstChild.before(icon);
        },

        setThisSemester: function() {
            var self = this;
            const firstdate = moment().startOf('quarter').format('YYYY-MM-DD');
            const lastdate = moment().endOf('quarter').format("YYYY-MM-DD");
            var dateFrom = self.el.querySelector('.datetimepicker-input[name="date_from"]')
            dateFrom.value = lastdate
            var dateTo = self.el.querySelector('.datetimepicker-input[name="date_to"]')
            dateTo.value = firstdate
            var checkDate = self.el.querySelector('#checkDate');
            checkDate.remove()
            var btn = self.el.querySelector('#thisSemester')
            var icon = document.createElement('i');
            icon.className = 'fa fa-solid fa-check'
            icon.style = 'color: #28a745;'
            icon.id = 'checkDate'
            btn.firstChild.before(icon);
        },

        setThisMonth: function() {
            var self = this;
            const firstdate = moment().startOf('month').format('YYYY-MM-DD');
            const lastdate = moment().endOf('month').format("YYYY-MM-DD");
            var dateFrom = self.el.querySelector('.datetimepicker-input[name="date_from"]')
            dateFrom.value = lastdate
            var dateTo = self.el.querySelector('.datetimepicker-input[name="date_to"]')
            dateTo.value = firstdate
            var checkDate = self.el.querySelector('#checkDate');
            checkDate.remove()
            var btn = self.el.querySelector('#thisMonth')
            var icon = document.createElement('i');
            icon.className = 'fa fa-solid fa-check'
            icon.style = 'color: #28a745;'
            icon.id = 'checkDate'
            btn.firstChild.before(icon);
            // self.el.querySelector('#setDates').textContent = "Este Mes";
        },

    });

    core.action_registry.add('account_extend_ikatech.action', OurAction);
    return OurAction;
});