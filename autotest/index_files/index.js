// JavaScript Document
$(function(){
	erMenu();
	bindLeftMenu();
	});
	
	
	function erMenu(){
		$(".navLi").mouseover(function(){
			$(this).find(".ermenu").show();
			})
		$(".navLi").mouseleave(function(){
			$(this).find(".ermenu").hide();
			})
		}
		
function bindLeftMenu()
{
	$(".menu li").click(function(){
				$(".menu li").removeClass("li_active2");
		$(this).addClass("li_active2");
		});
	$(".menu li div").click(function(){

		$(".menu li").find("div").removeClass("li_active");
		$(this).addClass("li_active");
		
		})
	}
		