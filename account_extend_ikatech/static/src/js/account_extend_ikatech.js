odoo.define('account_extend_ikatech.main', function (require) {

    const AbstractAction = require('web.AbstractAction');
    const core = require('web.core');

    var rpc = require('web.rpc');
    var QWeb = core.qweb;
    var time = require('web.time');

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
            'click #setDates': 'show_box_dates',
            'click .fourthDetailAmount': 'action_see_more_fourth',
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
            const filter_data_selected = {};
            if (initial_render) {
                filter_data_selected.date_from = moment().format('YYYY-MM-DD');
                filter_data_selected.date_to = moment().startOf('year').format('YYYY-MM-DD');
                // filter_data_selected.date_to = moment(date_to, time.getLangDateFormat()).locale('en').format('YYYY-MM-DD');
            } else {
                filter_data_selected.date_from = moment(new Date(this.$el.find('.datetimepicker-input[name="date_from"]').val()+"T00:00:00"), time.getLangDateFormat()).locale('en').format('YYYY-MM-DD');
                filter_data_selected.date_to = moment(new Date(this.$el.find('.datetimepicker-input[name="date_to"]').val()+"T00:00:00"), time.getLangDateFormat()).locale('en').format('YYYY-MM-DD');
                comparation = self.el.querySelector('#comparation').checked
                months = self.el.querySelector('#months').value
            }
            self._rpc({
                model: 'account.reports.pandl',
                method: 'pandl_report',
                args: [
                    [this.wizard_id, this.company_id, filter_data_selected, comparation, months], 
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
            const comparation = self.el.querySelector('#comparation').checked
            const months = self.el.querySelector('#months').value
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
                    args: [self.wizard_id, self.company_id, typeOp, idRow, date_from, date_to, comparation, months],
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
            const comparation = self.el.querySelector('#comparation').checked
            const months = self.el.querySelector('#months').value
            const accountId = el.target.getAttribute("idaccount") //por alguna razon trae la equiqueta span hija
            var type_operation = el.target.getAttribute("type_operation")
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
                    args: [self.wizard_id, self.company_id, accountId, date_from, date_to, comparation, months],
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
            if (months.value == 1){
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
    });

    core.action_registry.add('account_extend_ikatech.action', OurAction);
    return OurAction;
});