$(function () {
 
           var table = $('#mytable').DataTable({
               "dom": '<"top"f >rt<"bottom"ilp><"clear">',//dom定位
               "dom": 'tiprl',//自定义显示项
               //"dom":'<"domab"f>',
               "scrollY": "220px",//dt高度
               "lengthMenu": [
                   [8, 6, 8, -1],
                   [4, 6, 8, "All"]
               ],//每页显示条数设置
               "lengthChange": false,//是否允许用户自定义显示数量
               "bPaginate": true, //翻页功能
               "bFilter": false, //列筛序功能
               "searching": true,//本地搜索
               "ordering": true, //排序功能
               "Info": true,//页脚信息
               "autoWidth": true,//自动宽度
               "oLanguage": {//国际语言转化
                   "oAria": {
                       "sSortAscending": " - click/return to sort ascending",
                       "sSortDescending": " - click/return to sort descending"
                   },
                   "sLengthMenu": "show _MENU_ entries",
                   "sZeroRecords": "Sorry, NO query related data",
                   "sEmptyTable": "No related data",
                   "sLoadingRecords": "Loading...., Please wait",
                   "sInfo": "Showing _START_ to _END_ of _TOTAL_ entries。",
                   "sInfoEmpty": "The current show 0 to 0 entries, all is 0 entries",
                   "sInfoFiltered": "（Database includes _MAX_  entries）",
                   "sProcessing": "<img src='../resources/user_share/row_details/select2-spinner.gif'/> Date is loading...",
                   "sSearch": "Reserch：",
                   "sUrl": "",
                   //多语言配置文件，可将oLanguage的设置放在一个txt文件中，例：Javascript/datatable/dtCH.txt
                   "oPaginate": {
                       "sFirst": "First",
                       "sPrevious": " Previous ",
                       "sNext": " Next",
                       "sLast": " Last "
                   }
               },
 
               "columnDefs": [
                   {
                       orderable: false,
 
                       targets: 0 },
                   {
                       orderable: false,
 
                       targets: 1 }
               ],//第一列与第二列禁止排序
 
               "order": [
                   [0, null]
               ],//第一列排序图标改为默认
               initComplete: function () {//列筛选
                   var api = this.api();
                   api.columns().indexes().flatten().each(function (i) {
                       if (i != 0 && i != 1) {//删除第一列与第二列的筛选框
                           var column = api.column(i);
                           var $span = $('<span class="addselect">▾</span>').appendTo($(column.header()))
                           var select = $('<select><option value="">All</option></select>')
                                   .appendTo($(column.header()))
                                   .on('click', function (evt) {
                                       evt.stopPropagation();
                                       var val = $.fn.dataTable.util.escapeRegex(
                                               $(this).val()
                                       );
                                       column
                                               .search(val ? '^' + val + '$' : '', true, false)
                                               .draw();
                                   });
                           column.data().unique().sort().each(function (d, j) {
                               function delHtmlTag(str) {
                                   return str.replace(/<[^>]+>/g, "");//去掉html标签
                               }
 
                               d = delHtmlTag(d)
                               select.append('<option value="' + d + '">' + d + '</option>')
                               $span.append(select)
                           });
 
                       }
                   });
 
               }
 
           });
 
           //添加索引列
           table.on('order.dt search.dt',
                   function () {
                       table.column(0, {
                           search: 'applied',
                           order: 'applied'
                       }).nodes().each(function (cell, i) {
                           cell.innerHTML = i + 1;
                       });
                   }).draw();
 
           //自定义搜索
           $('.dsearch').on('keyup click', function () {
               var tsval = $(".dsearch").val()
               table.search(tsval, false, false).draw();
           });
 
           //checkbox全选
           $("#checkAll").on("click", function () {
               if ($(this).prop("checked") === true) {
                   $("input[name='checkList']").prop("checked", $(this).prop("checked"));
                   $('#mytable tbody tr').addClass('selected');
               } else {
                   $("input[name='checkList']").prop("checked", false);
                   $('#mytable tbody tr').removeClass('selected');
               }
           });
 
           //显示隐藏列
           $('.toggle-vis').on('change', function (e) {
               e.preventDefault();
               console.log($(this).attr('data-column'));
               var column = table.column($(this).attr('data-column'));
               column.visible(!column.visible());
           });
 
           //删除选中行
           $('#mytable tbody').on('click', 'tr input[name="checkList"]', function () {
               var $tr = $(this).parents('tr');
               $tr.toggleClass('selected');
               var $tmp = $('[name=checkList]:checkbox');
               $('#checkAll').prop('checked', $tmp.length == $tmp.filter(':checked').length);
 
           });
 
           $('#button').click(function () {
               table.row('.selected').remove().draw(false);
           });
 
           $('.showcol').click(function () {
               $('.showul').toggle();
 
           })
 
           //获取表格宽度赋值给右侧弹出层
           wt = $('.wt100').width();
           $('.showslider').css('right', -wt);
 
       })
 